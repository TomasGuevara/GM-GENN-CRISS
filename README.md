# GM-GENN-CRISS
---
## Sistema de generación narrativa interactiva controlado por restricciones semánticas mediante grafos de estados narrativos.

## Sistema para proveedor Ollama

## Sistema de prueba

En el motor de estudio  el sistema necesita que instales Llama en tu computadora 
y revises en la clase src.narrative_engine.getting_started.representarEstadoNarrativo
en en la linea donde se escribe la version de tu llm llama = Llama("llama3.1:8b").
Es importante que la descomentes y que dejes comentado el resto de proveedores, en la linea donde
se inicializa generator lo dejas como generator = NarrativeGenerator(llama).
Para poder hacer arrancar el motor de estudio es necesario escribir lo siguiente en la terminal
```
uv run python -m src.narrative_engine.getting_started.representarEstadoNarrativo
```
## Sistema completo aplicado

Para que el motor final funcione ademas de tener instalado Llama en tu computadora
debes revisar la clase src.narrative_engine.narrative_state.representNarrativeState
en la linea donde se escribe la version de tu llm llama = Llama("llama3.1:8b").
Es importante que la descomentes y que dejes comentado el resto de proveedores, en la linea donde
se inicializa generator lo dejas como generator = NarrativeGenerator(llama).
Para poder hacer arrancar el motor final es necesario escribir lo siguiente en la terminal
```
uv run python -m src.narrative_engine.main
```
---
## Sistema para proveedor Gemini

## Sistema de prueba

En el motor de estudio  el sistema necesita que instales Llama en tu computadora 
y revises en la clase src.narrative_engine.getting_started.representarEstadoNarrativo
en en la linea donde se escribe la version de tu llm gemini = Gemini("gemini-2.5-flash").
Es importante que la descomentes y que dejes comentado el resto de proveedores, en la linea donde
se inicializa generator lo dejas como generator = NarrativeGenerator(gemini).
Ademas tienes que cargar tu clave de gemini, para esto creas un archivo que se llame ".env" 
y dentro escribes.
```
GEMINI_API_KEY="AIzaSyTuClaveSecretaAqui"
```
Para poder hacer arrancar el motor de estudio es necesario escribir lo siguiente en la terminal
```
uv run python -m src.narrative_engine.getting_started.representarEstadoNarrativo
```
## Sistema completo aplicado

Para que el motor final funcione ademas de tener instalado Llama en tu computadora
debes revisar la clase src.narrative_engine.narrative_state.representNarrativeState
en en la linea donde se escribe la version de tu llm gemini = Gemini("gemini-2.5-flash").
Es importante que la descomentes y que dejes comentado el resto de proveedores, en la linea donde
se inicializa generator lo dejas como generator = NarrativeGenerator(gemini).
Ademas tienes que cargar tu clave de gemini, para esto creas un archivo que se llame ".env" 
y dentro escribes.
```
GEMINI_API_KEY="AIzaSyTuClaveSecretaAqui"
```
Para poder hacer arrancar el motor final es necesario escribir lo siguiente en la terminal
```
uv run python -m src.narrative_engine.main
```
