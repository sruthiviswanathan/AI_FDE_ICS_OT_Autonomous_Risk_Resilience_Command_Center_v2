# Current-State Architecture

```text
Enterprise IT / SOC / IAM / ERP
             |
            DMZ
      /       |        \
 Historian  Jump Host  MES Bridge
     |         |          |
  SCADA ---- Engineering -- CMMS/EAM
    |            |
 PLC/DCS ------ Gateways
    |            |
 Sensors      Field Devices
    |
 Physical Process

Parallel reality: vendor VPNs, service laptops, spreadsheets, shift notes and stale diagrams create undocumented paths.
```

There is no single system of cyber-physical truth and no verified end-to-end recovery graph.
