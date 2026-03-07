.PHONY: agent gateway test

agent:
	uvicorn agent.app.main:app --host 0.0.0.0 --port 8080 --reload

gateway:
	OPS_PULSE_AGENT_BASE_URL=http://localhost:8080 uvicorn gateway.app.main:app --host 0.0.0.0 --port 8090 --reload

test:
	pytest

