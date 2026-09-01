# GM-GENN-CRISS
---
## Sistema de generación narrativa interactiva controlado por restricciones semánticas mediante grafos de estados narrativos.

## Sistema de prueba

En el motor de estudio  el sistema necesita que instales Llama en tu computadora 
y revises en la clase src.narrative_engine.getting_started.representarEstadoNarrativo
en en la linea donde se escribe la version de tu llm llama = Llama("llama3.1:8b").
Para poder hacer arrancar el motor de estudio es necesario escribir lo siguiente en la terminal
```
uv run python -m src.narrative_engine.getting_started.representarEstadoNarrativo
```
## Sistema completo aplicado

Para que el motor final funcione ademas de tener instalado Llama en tu computadora
debes revisar la clase src.narrative_engine.narrative_state.representNarrativeState
en la linea donde se escribe la version de tu llm llama = Llama("llama3.1:8b").
Para poder hacer arrancar el motor de estudio es necesario escribir lo siguiente en la terminal
```
uv run python -m src.narrative_engine.main
```
