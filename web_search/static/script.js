window.onload = function() {
    // 在页面加载时禁用输入框
    document.getElementById('data').disabled = true;
};

function clearData() {
    fetch('/clear')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('output').innerHTML = '';
                document.getElementById('clearButton').style.display = 'none';
            }
        });
}

function refreshData() {
    document.getElementById('data').value = '';
}

function selectVersion(version) {
    fetch(`/select_version/${version}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateSelectedVersion(data.selected_version);
            }
        });
}

function updateSelectedVersion(version) {
    const buttons = document.querySelectorAll('.version-button');
    buttons.forEach(button => {
        button.classList.remove('selected');
        if (button.dataset.version === version) {
            button.classList.add('selected');
        }
    });

    const inputField = document.getElementById('data');
    inputField.disabled = version === null;

    if (version === null) {
        inputField.value = '';
    }

    document.getElementById('output').innerHTML = '';
    document.getElementById('clearButton').style.display = 'none';
}

function queryBalance() {
    const data = document.getElementById('data').value;

    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            version: document.querySelector('.selected').dataset.version,
            data: data
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            displayResults(data);
        }
    });
}

function displayResults(data) {
    const output = document.getElementById('output');
    output.innerHTML = '';
    for (const key in data) {
        output.innerHTML += `<p>${data[key]}</p>`;
    }
    document.getElementById('clearButton').style.display = 'block';
}