let message = document.querySelector('.copy-success-message-content')
if (message.innerText === "")
{
    console.log("empty")
}
else
{
    document.querySelector('.copy-success-message').style.display = 'block'
}


function selectText()
{
    let short_url = document.getElementById('short_url')
    if(short_url)
    {
        short_url.removeAttribute("disabled")
        short_url.setSelectionRange(0, 99999);
        short_url.select();
        short_url.setAttribute("disabled", "true")
    }
}



window.onload = selectText()

function copyShortUrl() 
{
    var copyText = document.getElementById("short_url");
    console.log(copyText)
    copyText.removeAttribute("disabled")
    copyText.setSelectionRange(0, 99999);
    copyText.select();
    document.execCommand("copy");
    copyText.setAttribute("disabled", "true")
    document.querySelector('.copy-success-message').style.display = 'block'
    document.querySelector('.copy-success-message-content').innerText = "URL Copied!"
}




function copyShortURLUser(id)
{
    console.log("Clicking from the User page.")
    // console.log("ID: ", id);
    let selector = "#hidden-" + id
    console.log(selector)
    let copyText = document.querySelector(selector);
    console.log(copyText)
    copyText.style.display = "block"
    copyText.setSelectionRange(0, 99999);
    copyText.select();
    document.execCommand("copy");
    copyText.style.display = "none"
    console.log("Copied text : ", copyText.value)
    document.querySelector('.message-'+id).style.display = 'block'
    document.querySelector('.message-content-'+id).innerText = "URL Copied!"
}
