ACTION_TIERS={
 "observe":0,"correlate":0,"summarize":0,"recommend":1,
 "request_fresh_telemetry":2,"open_ticket":2,"increase_logging":2,
 "isolate_endpoint":3,"change_remote_access":3,"change_firewall":3,
 "write_plc_logic":4,"change_setpoint":4,"modify_sis":4,"bypass_interlock":4,
}
def requires_human_approval(action:str)->bool:
    return ACTION_TIERS.get(action,4)>=3
