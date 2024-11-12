let elements = document.getElementsByClassName("btn btn-link");
for (let i = 0; i < elements.length; i++) {
    if (elements[i].tagName.toLowerCase() === 'a') {
        elements[i].click();
    }
}
document.getElementsByClassName("btn link-danger pull-left")[0].click();
document.getElementsByClassName("checkbox")[0].children[0].children[0].checked = true;
document.getElementsByClassName("btn btn-danger")[0].removeAttribute("disabled");
document.getElementsByClassName("btn btn-danger")[0].click();
