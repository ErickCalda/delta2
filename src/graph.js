import * as d3 from "d3";

let svg, x, y, plotArea;
let tangentLine, drLine, dvLine, pointHalo, pointDot;
let labelDr, labelDv;
// Nuevas variables para el Error Real
let pointReal, truncLine, labelTrunc; 

const width = 700;
const height = 450;
const margin = { top: 40, right: 60, bottom: 60, left: 80 };

const BLUE_CURVE = "#007AFF";
const YELLOW_LINE = "#F4B400";
const GREEN_DR = "#34A853";
const ORANGE_DV = "#FB8C00";
const RED_ERROR = "#E53935"; // Color para el error real

export function crearGrafico() {
    svg = d3.select("#graph").append("svg")
        .attr("width", width).attr("height", height)
        .style("background-color", "#FFFFFF");

    x = d3.scaleLinear().domain([0, 8]).range([margin.left, width - margin.right]);
    y = d3.scaleLinear().domain([0, 1300]).range([height - margin.bottom, margin.top]);

    // Máscara de recorte
    svg.append("defs").append("clipPath").attr("id", "plot-clip")
        .append("rect").attr("x", margin.left).attr("y", margin.top)
        .attr("width", width - margin.left - margin.right).attr("height", height - margin.top - margin.bottom);

    // Cuadrícula
    svg.append("g").attr("class", "grid")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x).ticks(8).tickSize(-height + margin.top + margin.bottom).tickFormat(""));
    svg.append("g").attr("class", "grid")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).ticks(6).tickSize(-width + margin.left + margin.right).tickFormat(""));

    // EJES CON NÚMEROS (Corregido para que se vean claros)
    svg.append("g").attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x).ticks(8)).attr("font-size", "14px");
    svg.append("g").attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).ticks(6)).attr("font-size", "14px");

    svg.append("text").attr("class", "axis-label").attr("x", width - margin.right + 10).attr("y", height - margin.bottom + 5).text("r(m)");
    svg.append("text").attr("class", "axis-label").attr("x", margin.left - 10).attr("y", margin.top - 15).attr("text-anchor", "middle").text("V(m³)");

    plotArea = svg.append("g").attr("clip-path", "url(#plot-clip)");

    // Curva Principal
    const V = r => (4 / 3) * Math.PI * Math.pow(r, 3);
    const data = d3.range(0, 8.1, 0.1).map(r => ({ r, v: V(r) }));

    plotArea.append("path").datum(data).attr("fill", "none").attr("stroke", BLUE_CURVE).attr("stroke-width", 5)
        .attr("d", d3.line().x(d => x(d.r)).y(d => y(d.v)));

    // Elementos base
    tangentLine = plotArea.append("line").attr("stroke", YELLOW_LINE).attr("stroke-width", 4);
    drLine = plotArea.append("line").attr("stroke", GREEN_DR).attr("stroke-width", 3).attr("stroke-dasharray", "6,6");
    dvLine = plotArea.append("line").attr("stroke", ORANGE_DV).attr("stroke-width", 3).attr("stroke-dasharray", "6,6");
    
    // === NUEVOS ELEMENTOS DE ERROR REAL ===
    truncLine = plotArea.append("line").attr("stroke", RED_ERROR).attr("stroke-width", 3).attr("stroke-dasharray", "4,4");
    pointReal = plotArea.append("circle").attr("r", 6).attr("fill", RED_ERROR);

    pointHalo = plotArea.append("circle").attr("r", 12).attr("fill", "none").attr("stroke", "gray").attr("stroke-width", 2);
    pointDot = plotArea.append("circle").attr("r", 5).attr("fill", "black");

    labelDr = svg.append("text").attr("class", "math-text").attr("fill", GREEN_DR).attr("text-anchor", "middle");
    labelDv = svg.append("text").attr("class", "math-text").attr("fill", ORANGE_DV);
    labelTrunc = svg.append("text").attr("class", "math-text").attr("fill", RED_ERROR);
}

// 5. Recibimos el parámetro 'mostrarErrorReal'
export function actualizarGrafico(r0, dr, mostrarErrorReal = false) {
    const V = r => (4 / 3) * Math.PI * Math.pow(r, 3);
    
    const v0 = V(r0);
    const pendiente = 4 * Math.PI * Math.pow(r0, 2);
    const r_error = r0 + dr;
    
    const v_aprox = v0 + pendiente * (r_error - r0);
    const v_real = V(r_error); // El volumen exacto en la curva azul

    pointHalo.attr("cx", x(r0)).attr("cy", y(v0));
    pointDot.attr("cx", x(r0)).attr("cy", y(v0));

    tangentLine.attr("x1", x(0)).attr("y1", y(v0 + pendiente * (0 - r0)))
               .attr("x2", x(8)).attr("y2", y(v0 + pendiente * (8 - r0)));

    drLine.attr("x1", x(r0)).attr("y1", y(v0)).attr("x2", x(r_error)).attr("y2", y(v0));
    dvLine.attr("x1", x(r_error)).attr("y1", y(v0)).attr("x2", x(r_error)).attr("y2", y(v_aprox));

    labelDr.attr("x", x(r0 + dr / 2)).attr("y", y(v0) + 20).text(`dr = ${dr.toFixed(1)}m`);
    labelDv.attr("x", x(r_error) + 10).attr("y", y((v0 + v_aprox) / 2)).text("dV");

   // === ACTUALIZACIÓN DEL ERROR REAL ===
    // Ubicamos el punto rojo y la línea que conecta la aproximación con la curva real
    pointReal.attr("cx", x(r_error)).attr("cy", y(v_real));
    truncLine.attr("x1", x(r_error)).attr("y1", y(v_aprox)).attr("x2", x(r_error)).attr("y2", y(v_real));
    
    // 1. Calculamos el valor numérico del error (valor absoluto de la diferencia)
    const errorNum = Math.abs(v_real - v_aprox);

    // 2. Actualizamos la etiqueta para mostrar el número con 1 decimal
    labelTrunc.attr("x", x(r_error) + 10)
              .attr("y", y((v_aprox + v_real) / 2))
              .text(`Falla: ${errorNum.toFixed(1)} m³`);
    // === LÓGICA DE VISIBILIDAD ===
    // Si el checkbox está marcado, opacidad es 1 (visible), si no, 0 (oculto).
    // Usamos transiciones suaves para que aparezca y desaparezca elegantemente.
    const opacidad = mostrarErrorReal ? 1 : 0;
    pointReal.transition().duration(200).attr("opacity", opacidad);
    truncLine.transition().duration(200).attr("opacity", opacidad);
    labelTrunc.transition().duration(200).attr("opacity", opacidad);
}