document.addEventListener('DOMContentLoaded', function () {
    console.log('Admin Translate JS Loaded');

    function createGenerateButton(targetFieldId, sourceFieldId) {
        const targetField = document.getElementById(targetFieldId);
        const sourceField = document.getElementById(sourceFieldId);

        if (!targetField || !sourceField) return;

        // Check if button already exists
        if (targetField.parentNode.querySelector('.btn-translate')) return;

        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn btn-sm btn-info ml-2 btn-translate';
        btn.innerHTML = '✨ Generatsiya';
        btn.style.marginTop = '5px';
        btn.style.padding = '4px 8px';
        btn.style.cursor = 'pointer';

        btn.onclick = async function () {
            const uzText = sourceField.value;
            if (!uzText) {
                alert('Iltimos, avval uz maydonini to\'ldiring!');
                return;
            }

            btn.disabled = true;
            btn.innerHTML = '⌛ Tarjima qilinmoqda...';

            try {
                const response = await fetch('/api/products/translate/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ text: uzText })
                });

                const data = await response.json();
                if (data.translated_text) {
                    targetField.value = data.translated_text;
                    targetField.style.backgroundColor = '#e8f0fe';
                } else if (data.error) {
                    alert('Xatolik: ' + data.error);
                }
            } catch (error) {
                console.error('Translation error:', error);
                alert('Tarjima qilishda xatolik yuz berdi.');
            } finally {
                btn.disabled = false;
                btn.innerHTML = '✨ Generatsiya';
            }
        };

        targetField.parentNode.appendChild(btn);
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Product Fields
    createGenerateButton('id_name_ru', 'id_name');
    createGenerateButton('id_description_ru', 'id_description');

    // Category Fields
    createGenerateButton('id_name_ru', 'id_name');
});
