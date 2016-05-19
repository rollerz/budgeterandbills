$(document).ready(function() {
    $('#log').validate({
        rules: {
            loginUser: {
                required: true,
                minlength: 5
            },
            loginPass: {
                required: true,
                minlength: 8
            }
        },
        messages: {
            loginUser: {
                required: "Please enter your username!",
                minlength: "Usernames are at least 5 characters!"
            },
            loginPass: {
                required: "Please enter your password!",
                minlength: "Passwords are at least 8 characters!"
            }
        },
        errorElement: "span",
        wrapper: "span"
    });
    $('#reg').validate({
        rules: {
            user: {
                required: true,
                minlength: 5
            },
            pass: {
                required: true,
                minlength: 8
            },
            conf: {
                required: true,
                equalTo: "#pass",
                minlength: 8
            }
        },
        messages: {
            user: {
                required: "Please enter a username!",
                minlength: "Usernames must be at least 5 characters!"
            },
            pass: {
                required: "Please enter a password!",
                minlength: "Passwords must be at least 8 characters!"
            },
            conf: {
                required: "Please confirm your password!",
                equalTo: "Your passwords do not match!",
                minlength: "Passwords must be at least 8 characters!"
            }
        },
        errorElement: "span",
        wrapper: "span"
    });
    $('#new').validate({
        rules: {
            bName: {
                required: true,
                minlength: 2
            },
            bDate: "required",
            bRep: {
                required: true
            },
            bAmt: {
                required: true,
                number: true
            }
        },
        messages: {
            bName: {
                required: "Please enter the bill name!",
                minlength: "Bill name must be greater than 2 characters!"
            },
            bDate: "Please enter the due date!",
            bRep: "Please select a reccurence!",
            bAmt: {
                required: "Please enter the billing amount due!",
                number: "Your billing amount is not a number!"
            }
        },
        errorElement: "span",
        wrapper: "span"
    });
    $('#upd').validate({
        rules: {},
        messages: {},
        errorElement: "div",
        wrapper: "div"
    });
    $('.inp').each(function() {
        $(this).rules('add', {
            required: true,
            number: true,
            messages: {
                required: "Please enter a number in the box!",
                number: "Your entry is not a number!"
            },
        });
    });
});
