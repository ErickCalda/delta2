import "./styles.css";
import { crearGrafico, actualizarGrafico } from "./graph.js";
import { volumen, diferencial, porcentaje } from "./math.js";

// Inicializamos solo el gráfico (nada de escena 3D)
crearGrafico();

const radio = document.getElementById("radio");
const dr = document.getElementById("dr");
const checkboxError = document.getElementById("toggle-error-real");

let ticking = false;

function actualizar() {
    const r = parseFloat(radio.value);
    const error = parseFloat(dr.value);
    const mostrarErrorReal = checkboxError.checked;

    // 1. Textos de los sliders
    document.getElementById("radio-value").textContent = r.toFixed(1);
    document.getElementById("dr-value").textContent = error.toFixed(1);

    // 2. Cálculos matemáticos
    const V = volumen(r);
    const dV = diferencial(r, error);

    const vRealExacto = volumen(r + error);
    const deltaV = vRealExacto - V;         
    const errorTruncamiento = Math.abs(deltaV - dV);

    // 3. Actualización de las tarjetas de resultados
    document.getElementById("volumen").textContent = V.toFixed(2) + " m³";
    document.getElementById("dv").textContent = dV.toFixed(2) + " m³";
    document.getElementById("error").textContent = porcentaje(V, dV).toFixed(2) + "%";

    const panelTruncamiento = document.getElementById("error-truncamiento");
    if (panelTruncamiento) {
        panelTruncamiento.textContent = errorTruncamiento.toFixed(2) + " m³";
    }
    
    // 4. Actualizamos la gráfica
    actualizarGrafico(r, error, mostrarErrorReal);

    ticking = false;
}

function manejarInput() {
    if (!ticking) {
        requestAnimationFrame(actualizar);
        ticking = true;
    }
}

// Listeners
radio.addEventListener("input", manejarInput);
dr.addEventListener("input", manejarInput);
checkboxError.addEventListener("change", manejarInput);

// Primera llamada para inicializar la vista
actualizar();