document.addEventListener('DOMContentLoaded', function () {
    console.log('Admin Translate JS Loaded');

    function createGenerateButton(targetFieldId, sourceFieldId) {
        const targetField = document.getElementById(targetFieldId);
        const sourceField = document.getElementById(sourceFieldId);

        if (!targetField || !sourceField) return;

        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn btn-sm btn-info ml-2';
        btn.innerHTML = '<i class="fas fa-magic"></i> Generate RU';
        btn.style.marginTop = '5px';

        btn.onclick = function () {
            const uzText = sourceField.value;
            if (!uzText) {
                alert('Iltimos, avval uz maydonini to\'ldiring!');
                return;
            }

            // Simple mock translation / hint
            // In a real app, you'd call a translation API here
            targetField.value = uzText + ' (RU)';
            targetField.style.backgroundColor = '#e8f0fe';

            console.log('Generating RU for:', uzText);

            // Optional: provide a link to Google Translate for manual copy
            window.open(`https://translate.google.com/?sl=uz&tl=ru&text=${encodeURIComponent(uzText)}&op=translate`, '_blank');
        };

        targetField.parentNode.appendChild(btn);
    }

    // Product Fields
    createGenerateButton('id_name_ru', 'id_name');
    createGenerateButton('id_description_ru', 'id_description');

    // Category Fields
    createGenerateButton('id_name_ru', 'id_name');
});
