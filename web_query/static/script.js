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

let selectedVersion = null;
function selectVersion(version) {
    selectedVersion = version;
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


function queryBalance(data, version) {
    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            type: 'purchase',
            version: version,
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

function queryFunction(data, version) {
    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            type: 'feature',
            version: version,
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

function queryAll(data, version) {
    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            type: 'all',
            version: version,
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

function handleQuery() {
    const data = document.getElementById('data').value;
    const selectElement = document.getElementById('queryType');
    const selectedValue = selectElement.value;

    if (selectedVersion === null) {
        alert('请先选择bot购买的版本');
        return;
    }

    if (!data) {
        alert('请输入您的qq号');
        return;
    }

    if (selectedValue === 'purchase') {
        queryBalance(data, selectedVersion);
    } else if (selectedValue === 'feature') {
        queryFunction(data, selectedVersion);
    } else {
        queryAll(data, selectedVersion);
    }
}


function refreshData() {
    document.getElementById('data').value = '';
// 默认为ALL，都查询
    document.getElementById('queryType').value = 'all';
    selectVersion = null;
    alert('已清空输入和选择');
}



function displayResults(data) {
    const output = document.getElementById('output');
    output.innerHTML = '';
    for (const key in data) {
        output.innerHTML += `<p>${data[key]}</p>`;
    }
    document.getElementById('clearButton').style.display = 'block';
}