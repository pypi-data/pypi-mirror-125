from .SwitchDTO import Switch
from .SwitchConsequentFunctions import SwitchConsequentFunction
from ..DeviceEvaluationDTO import DeviceEvaluation


class SwitchFunction(object):
    def __init__(self, redis):
        self.r = redis
        self.switch_consequent_functions = SwitchConsequentFunction(redis)

    def register(self, user_id, device_id):
        try:
            result = "false"
            key_pattern = "device:" + device_id
            if self.r.exists(key_pattern + ":name") == 0:
                self.r.rpush("user:" + user_id + ":switches", device_id)
                device_id_keys = self.r.lrange("user:" + user_id + ":switches")
                device = Switch()
                device.id = device_id
                device.name = "SWITCH " + str(len(device_id_keys))
                self.r.set(key_pattern + ":name", device.name)
                self.r.set(key_pattern + ":user_id", user_id)
                self.r.set(key_pattern + ":measure", device.measure)
                self.r.set(key_pattern + ":last_date_on", device.last_date_on)
                self.r.set(key_pattern + ":last_date_off", device.last_date_off)
                self.r.set(key_pattern + ":last_time_on", device.last_time_on)
                self.r.set(key_pattern + ":last_time_off", device.last_time_off)
                self.r.set(key_pattern + ":automatic", device.automatic)
                self.r.set(key_pattern + ":manual_measure", device.manual_measure)
                result = device
            return result
        except Exception as error:
            print(repr(error))
            return "error"

    def get_device(self, user_id, device_id):
        try:
            key_pattern = "device:" + device_id
            dto = Switch()
            dto.id = device_id
            dto.name = self.r.get(key_pattern + ":name")
            dto.automatic = self.r.get(key_pattern + ":automatic")
            dto.manual_measure = self.r.get(key_pattern + ":manual_measure")
            dto.last_date_on = self.r.get(key_pattern + ":last_date_on")
            dto.last_date_off = self.r.get(key_pattern + ":last_date_off")
            dto.last_time_on = self.r.get(key_pattern + ":last_time_on")
            dto.last_time_off = self.r.get(key_pattern + ":last_time_off")
            if self.r.exists(key_pattern + ":rules") == 1:
                rules_id = self.r.lrange(key_pattern + ":rules")
                for rule_id in rules_id:
                    rule_name = self.r.get("user:" + user_id + ":rule:" + rule_id + ":name")
                    dto.rules.append({"id": rule_id, "name": rule_name})
            if self.r.exists(key_pattern + ":measure") == 1:
                measure = self.r.get(key_pattern + ":measure")
                if measure == "-":
                    dto.measure = measure
                    dto.color = "yellow"
                    dto.status = "initialization"
                else:
                    dto.measure = measure
                    dto.color = "green"
                    dto.status = "connected"
            return dto
        except Exception as error:
            print(repr(error))
            return "error"

    def update_device(self, new_device):
        try:
            dto = Switch()
            dto.device_mapping(new_device)
            key_pattern = "device:" + dto.id
            self.r.set(key_pattern + ":name", dto.name)
            self.r.set(key_pattern + ":automatic", dto.automatic)
            self.r.set(key_pattern + ":manual_measure", dto.manual_measure)
            return dto
        except Exception as error:
            print(repr(error))
            return "error"

    def delete_device(self, user_id, device_id):
        try:
            self.r.lrem("user:" + user_id + ":switches", device_id)
            key_pattern = "device:" + device_id
            self.r.delete(key_pattern + ":name")
            self.r.delete(key_pattern + ":user_id")
            self.r.delete(key_pattern + ":measure")
            self.r.delete(key_pattern + ":manual_measure")
            self.r.delete(key_pattern + ":automatic")
            self.r.delete(key_pattern + ":last_date_on")
            self.r.delete(key_pattern + ":last_date_off")
            self.r.delete(key_pattern + ":last_time_on")
            self.r.delete(key_pattern + ":last_time_off")
            if self.r.exists(key_pattern + ":rules") == 1:
                rules = self.r.lrange(key_pattern + ":rules")
                for rule_id in rules:
                    self.switch_consequent_functions.delete_consequent(user_id, rule_id, device_id)
            return "true"
        except Exception as error:
            print(repr(error))
            return "error"

    def device_evaluation(self, device_id):
        output = DeviceEvaluation()
        key_pattern = "device:" + device_id
        if self.r.exists(key_pattern + ":user_id") == 1:
            user_id = self.r.get("device:" + device_id + ":user_id")
            output.user_id = user_id
            output.device_id = device_id
            output.type = "consequent"
            output.measure = self.measure_evaluation(user_id, device_id)
        return output

    def measure_evaluation(self, user_id, device_id):
        key_pattern = "device:" + device_id
        automatic = self.r.get(key_pattern + ":automatic")
        if automatic == "true":
            rules = list(self.r.smembers(key_pattern + ":rules"))
            status = "off"
            for rule in rules:
                if self.r.get("user:" + user_id + ":rule:" + rule + ":evaluation") == "true":
                    status = "on"
                    break
        else:
            status = self.r.get(key_pattern+":manual_measure")
        return status


