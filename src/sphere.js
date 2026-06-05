import * as THREE from "three";

let sphere;

export function crearEscena() {

    const container =
        document.getElementById("sphere");

    const scene = new THREE.Scene();

    const camera =
        new THREE.PerspectiveCamera(
            75,
            container.clientWidth /
            container.clientHeight,
            0.1,
            1000
        );

    const renderer =
        new THREE.WebGLRenderer({
            antialias:true
        });

    renderer.setSize(
        container.clientWidth,
        container.clientHeight
    );

    container.appendChild(
        renderer.domElement
    );

    const geometry =
        new THREE.SphereGeometry(
            1,
            64,
            64
        );

    const material =
        new THREE.MeshStandardMaterial({
            color:0x2563eb
        });

    sphere =
        new THREE.Mesh(
            geometry,
            material
        );

    scene.add(sphere);

    const light =
        new THREE.DirectionalLight(
            0xffffff,
            2
        );

    light.position.set(5,5,5);

    scene.add(light);

    camera.position.z = 8;

    function animate() {

        requestAnimationFrame(animate);

        sphere.rotation.y += 0.01;

        renderer.render(
            scene,
            camera
        );
    }

    animate();
}

export function actualizarEsfera(radio)
{
    if(!sphere) return;

    sphere.scale.set(
        radio/4,
        radio/4,
        radio/4
    );
}