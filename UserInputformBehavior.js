function updateFormVisibility() {
    const printingType = document.querySelector('input[name="printing_type"]:checked')?.value;
    const isFDM = printingType === 'FDM';
    const isSLA = printingType === 'SLA';

    // Update FDM related sections
    const infillSection = document.getElementById('infillPercentageSection');
    infillSection.classList.toggle('disabled-section', !isFDM);
    infillSection.querySelectorAll('input').forEach(input => input.disabled = !isFDM);

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
    const infillValue = document.querySelector('input[name="infill_percentage"]').value;
    document.getElementById('infillPercentageValue').textContent = infillValue;
}

document.addEventListener('DOMContentLoaded', function() {
    updateFormVisibility(); // Update form visibility based on selected printing type
    updateInfillPercentageValue(); // Set initial infill percentage value
});

// Event listener for infill percentage slider
const infillSlider = document.getElementById('infillPercentageSlider');
if (infillSlider) {
    infillSlider.addEventListener('input', updateInfillPercentageValue);
}

document.addEventListener('DOMContentLoaded', function() {
    // Existing initialization code

    const quantityInput = document.querySelector('input[name="quantity"]');
    document.getElementById('button-minus').addEventListener('click', function() {
        if (quantityInput.value > 0) {
            quantityInput.value = parseInt(quantityInput.value) - 1;
        }
    });

    document.getElementById('button-plus').addEventListener('click', function() {
        quantityInput.value = parseInt(quantityInput.value) + 1;
    });
});
