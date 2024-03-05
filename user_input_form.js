function updateFormVisibility() {
    const printingType = document.querySelector('input[name="printing_type"]:checked')?.value;
    const isFDM = printingType === 'FDM';
    const isSLA = printingType === 'SLA';

    // Update FDM related sections
    const infillSection = document.getElementById('infillPercentageSection');
    infillSection.classList.toggle('disabled-section', !isFDM);
    infillSection.querySelector('input').disabled = !isFDM;

    // Update SLA related sections
    const fillTypeSection = document.getElementById('fillTypeSection');
    fillTypeSection.classList.toggle('disabled-section', !isSLA);
    fillTypeSection.querySelectorAll('input').forEach(input => input.disabled = !isSLA);

    // Update Material Selection Section
    const materialSelectionSection = document.getElementById('materialSelectionSection');
    materialSelectionSection.classList.toggle('disabled-section', !isFDM);
    materialSelectionSection.querySelector('select').disabled = !isFDM;
}

function updateInfillPercentageValue() {
    const infillValue = document.getElementById('infillPercentageSlider').value;
    document.getElementById('infillPercentageValue').textContent = infillValue;
}

document.addEventListener('DOMContentLoaded', function() {
    updateFormVisibility(); // Update form visibility based on selected printing type
    updateInfillPercentageValue(); // Set initial infill percentage value

    // Event listeners for form visibility and infill percentage slider
    document.querySelectorAll('input[name="printing_type"]').forEach(input => {
        input.addEventListener('change', updateFormVisibility);
    });
    document.getElementById('infillPercentageSlider').addEventListener('input', updateInfillPercentageValue);

    // Quantity increment and decrement buttons
    const quantityInput = document.querySelector('input[name="quantity"]');
    document.getElementById('button-minus').addEventListener('click', function() {
        if (quantityInput.value > 0) {
            quantityInput.value = parseInt(quantityInput.value) - 1;
        }
    });

    document.getElementById('button-plus').addEventListener('click', function() {
        quantityInput.value = parseInt(quantityInput.value) + 1;
    });

    // File input change event for model display
    document.getElementById('userFile').addEventListener('change', function(event) {
        if (event.target.files[0]) {
            displayModel(event.target.files[0]);
            // Update the file name display
            document.getElementById('fileNameDisplay').textContent = event.target.files[0].name;
        }
    });
});

function displayModel(file) {
    const container = document.getElementById('modelDisplayContainer');
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setClearColor(0x333333); // Setting a background color for visibility
    renderer.setSize(container.clientWidth, 500); // Ensure this matches the container's height
    container.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / 500, 0.1, 2000);

    const ambientLight = new THREE.AmbientLight(0x404040); // Soft white light
    scene.add(ambientLight);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1.0);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);

    const loader = new THREE.STLLoader();
    loader.load(URL.createObjectURL(file), function (geometry) {
        const material = new THREE.MeshPhongMaterial({ color: 0xff5533, specular: 0x111111, shininess: 200 });
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        // Adjust camera and controls based on the loaded model
        geometry.computeBoundingBox();
        const boundingBox = geometry.boundingBox;
        const center = boundingBox.getCenter(new THREE.Vector3());
        const size = boundingBox.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);
        const fov = camera.fov * (Math.PI / 180);
        let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
        cameraZ *= 1.5; // Adjust camera distance
        camera.position.z = cameraZ;

        camera.lookAt(center); // Ensure the camera looks at the model

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.target.copy(center);
        controls.update();

        function animate() {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }
        animate();
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('quoteForm');
form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(form);
    const fileInput = document.getElementById('userFile');
    if (fileInput.files.length > 0) {
        formData.append('stl_file', fileInput.files[0]);
    }

    // Debugging: Log each key-value pair in the FormData
    for (let [key, value] of formData.entries()) {
        console.log('FormData key-value pair:', key, value);
    }

    const bearerToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkpvaG4uZG9lIiwiZW1haWwiOiJKb2huQGdtYWlsLmNvbSIsInVzZXJfaWQiOjEsInJvbGUiOiJBRE1JTiIsImlhdCI6MTcwOTMxNjAwMSwiZXhwIjoxNzA5MzI2ODAxfQ.NuHjzRY4oO8UA5PJ29x55qHROdNxcCe4fsgFm8W9-4U';

    axios.post('http://52.14.171.52:3000/api/create-quote', formData, {
        headers: {
            'Authorization': `Bearer ${bearerToken}`,
            // 'Accept' and 'Accept-Language' can be set as needed
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.8',
            // Do not manually set 'Content-Type' for multipart/form-data
        },
    })


        // axios({
        //     method: 'post',
        //     url: 'http://52.14.171.52:3000/api/create-quote',
        //     data: formData,
        //     headers: {
        //         'Authorization': `Bearer ${bearerToken}`,
        //         //'Content-Type': 'multipart/form-data'
        //     },
        // })
        .then(function(response) {
            console.log('Raw response:', response);
            // Update the UI with the server response
            const responseDisplay = document.getElementById('responseDisplay');
            responseDisplay.textContent = "Response: " + JSON.stringify(response.data);
        })
        .catch(function(error) {
            console.error('Axios request failed: ', error.toJSON());
            const responseDisplay = document.getElementById('responseDisplay');
            if(error.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                responseDisplay.textContent = "Error: " + JSON.stringify(error.response.data);
            } else if(error.request) {
                // The request was made but no response was received
                responseDisplay.textContent = "Error: The request was made but no response was received";
            } else {
                // Something happened in setting up the request that triggered an Error
                responseDisplay.textContent = "Error: " + error.message;
            }
        });
    });
});




