var selectedCategory = '';
        var previousButton = null;  // Add this line

        function refreshData() {
            document.getElementById('key').value = '';
        }

        function setCategory(category, button) {
            selectedCategory = category;
            //选择按钮后才可以输入key和qq
            document.getElementById("key").disabled = false;
            document.getElementById("qq").disabled = false;
            document.querySelector("button[onclick='verifyKey()']").disabled = false;
            if (previousButton) {
                previousButton.classList.remove('selected');  // Remove highlight from previous button
            }
            button.classList.add('selected');  // Highlight the clicked button
            previousButton = button;  // Update the previousButton reference
        }

        function verifyKey() {
            var qq = document.getElementById('qq').value;
            var key = document.getElementById('key').value;
            //key值不能为空，qq只能输入5-13位数字且开头不为0
            if (key.trim() === "") {
                alert("密钥不能为空！");
                return;
            }
            if (qq.trim() === "") {
                alert("qq号不能为空！");
                return;
            }
            if (!qq.match(/^[1-9]\d{4,12}$/)) {
                alert("请检查qq号拼写~");
                return;
            }
            fetch('/verify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    qq: qq,
                    category: selectedCategory,
                    key: key,
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.verified) {
                    alert("密钥验证成功(●'u'●)~约等待1小时候即可正常对话。如不能正常对话，可以查询一下自己的额度，如果额度信息已经更新，说明额度添加正常，只是由于服务器性能不好导致更新缓慢，请耐心等待。最长需要等待一个晚上。\n\n p.s.券已经验证，后面【不可二次使用】啦");
                } else {
                    if(selectedCategory ==''){
                        alert('请选择购买bot老公类型!');
                    }else{
                        alert('密钥【可能】验证失败了，请关闭弹窗后在本页面下方点击一下【额度查询】!如果查到了自己的购买信息，即为【验证成功】。\n\n 如果查不到请检查老公是否选择错误、密钥是否复制错误（可以再试一遍TAT？）');
                    }
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
