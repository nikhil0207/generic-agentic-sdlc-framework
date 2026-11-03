---
agent: 00-sdlc-orchestrator
description: Start a governed defect or VSTS work-item workflow.
---
Create or resume a DEFECT workflow for ticket ${input:ticket}. If Azure DevOps is configured, retrieve it read-only; otherwise request supplied ticket content. Require root-cause and regression evidence and never close the ticket automatically.
