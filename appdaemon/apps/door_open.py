import appdaemon.appapi as appapi


class DoorLight(appapi.AppDaemon):
  def initialize(self):
    if "door_sensor" in self.args:
      for sensor in self.split_device_list(self.args["door_sensor"]):
        self.listen_state(self.state_change, sensor)
    

  def state_change(self, entity, attribute, old, new, kwargs):
    if new == "Open" and self.get_state(self.args["light"]) == "off":
      self.turn_on(self.args["light"])
      self.log("Door Open, Light On")
      self.run_in(self.light_off, self.args["time_on"])
    elif new == "Open" and self.get_state(self.args["light"]) == "on":
      pass


  def light_off(self, kwargs):
    self.log("Light Off")
    self.turn_off(self.args["light"])


class DoorNotify(appapi.AppDaemon):
  def initialize(self):
    if "door_sensor" in self.args:
      for sensor in self.split_device_list(self.args["door_sensor"]):
        self.listen_state(self.state_change, sensor)

  def state_change(self, entity, attribute, old, new, kwargs):
    if entity == "sensor.front_door_status" and new == "Open" and self.get_state("input_boolean.door_notify") == "on":
      self.call_service("notify/notify_push_android", title = "Home Assistant", message = "Front Door Opened")
    elif entity == "sensor.back_door_status" and new == "Open" and self.get_state("input_boolean.door_notify") == "on":
      self.call_service("notify/notify_push_android", title = "Home Assistant", message = "Back Door Opened")