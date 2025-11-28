# Guía de Instalación y Uso de Tailwind CSS

## 📦 Instalación Completada

Tailwind CSS ha sido instalado exitosamente en tu proyecto Flask.

## 📁 Archivos Creados

1. **`package.json`** - Configuración de npm con scripts
2. **`tailwind.config.js`** - Configuración de Tailwind
3. **`static/css/input.css`** - Archivo de entrada con estilos personalizados
4. **`static/css/output.css`** - Archivo compilado (generado automáticamente)
5. **`templates/base.html`** - Template base con Tailwind

## 🎨 Colores Personalizados

Se configuró una paleta de colores verde para el tema deportivo:

```html
<!-- Ejemplos de uso -->
<button class="bg-primary-600 hover:bg-primary-700">Botón</button>
<div class="text-primary-500">Texto verde</div>
```

## 🛠️ Componentes Personalizados

### Botones
```html
<button class="btn-primary">Botón Principal</button>
<button class="btn-secondary">Botón Secundario</button>
```

### Tarjetas
```html
<div class="card">Contenido de la tarjeta</div>
<div class="cancha-card">Tarjeta de cancha</div>
```

### Campos de Entrada
```html
<input type="text" class="input-field" placeholder="Nombre">
```

## 🚀 Comandos Disponibles

### Modo Desarrollo (con watch)
```bash
npm run dev
```
Este comando observa cambios en tus archivos HTML y regenera el CSS automáticamente.

### Compilar para Producción
```bash
npm run build
```
Genera un archivo CSS minificado para producción.

## 📝 Cómo Usar en tus Templates

### 1. Extender el template base
```html
{% extends "base.html" %}

{% block title %}Mi Página{% endblock %}

{% block content %}
    <h1 class="text-3xl font-bold text-gray-900">Hola Mundo</h1>
{% endblock %}
```

### 2. Ejemplo de página con Tailwind
```html
{% extends "base.html" %}

{% block content %}
<div class="container mx-auto">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="cancha-card">
            <img src="..." class="w-full h-48 object-cover">
            <div class="p-4">
                <h3 class="text-xl font-bold mb-2">Cancha 1</h3>
                <p class="text-gray-600">Descripción...</p>
                <button class="btn-primary mt-4">Reservar</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## 🔄 Workflow Recomendado

1. **Inicia el servidor Flask**:
   ```bash
   python app.py
   ```

2. **En otra terminal, inicia Tailwind en modo watch**:
   ```bash
   npm run dev
   ```

3. **Edita tus templates HTML** con clases de Tailwind

4. **Los cambios se reflejarán automáticamente** al recargar el navegador

## 📚 Recursos Útiles

- [Documentación de Tailwind CSS](https://tailwindcss.com/docs)
- [Cheat Sheet](https://nerdcave.com/tailwind-cheat-sheet)
- [Tailwind UI Components](https://tailwindui.com/components)

## ⚠️ Importante

- El archivo `static/css/output.css` es generado automáticamente, **NO lo edites manualmente**
- Todos los estilos personalizados van en `static/css/input.css`
- Asegúrate de incluir `{% extends "base.html" %}` en tus templates para usar Tailwind
