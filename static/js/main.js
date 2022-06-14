$('#loginForm').submit(function (event) {
    event.preventDefault();
    const form = {
        email: $('#loginEmail').val(),
        password: $('#loginPassword').val(),
    };
    console.log('[登入]', form);
});

$('#signUpForm').submit(function (event) {
    event.preventDefault();
    const form = {
        email: $('#signUpEmail').val(),
        password: $('#signUpPassword').val(),
    };
    console.log('[註冊]', form);
});

$('#logoutBtn').click(function () {
    console.log('[登出]');
});