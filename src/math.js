export function volumen(r) {
    return (4 / 3) * Math.PI * Math.pow(r, 3);
}

export function diferencial(r, dr) {
    return 4 * Math.PI * Math.pow(r, 2) * dr;
}

export function porcentaje(v, dv) {
    return (dv / v) * 100;
}