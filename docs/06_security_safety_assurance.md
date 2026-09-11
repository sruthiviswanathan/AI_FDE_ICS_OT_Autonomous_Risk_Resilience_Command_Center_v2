# Security, Safety and Assurance Constraints

Allowed autonomous behavior: collect, correlate, enrich, summarize, rank evidence and run read-only simulation.

Potentially policy-controlled reversible behavior in a real implementation: request fresh telemetry, open ticket, increase logging, capture evidence.

Human-authorized consequential behavior: network isolation, remote-access changes, firewall policy changes, maintenance-mode transitions.

Out of scope for this repository and generally highly restricted: PLC logic writes, setpoint changes, SIS modifications, interlock bypass, trip suppression, unsafe restart.

Every recommendation should expose evidence, freshness, uncertainty, process impact, safety impact, rollback considerations and required authority.
