const isInViewport = function (el) {

    const style = getComputedStyle(el)
    if (style.display != 'none') {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }
}

const postToBackend = (endpoint, banner_id, payload) => {

    var csfr_token = document.getElementsByName("csrfmiddlewaretoken")[0].value    
    window.fetch(`${API_ENDPOINT}/${banner_id}/${endpoint}`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csfr_token
        },
        body: JSON.stringify(payload)
    }).then((data) => {
        return data.json();
    }).catch((error) => {
        console.log(error)
    })
}

function init_ads() {

    let trigger_elements = [];
    let advertisements;

    advertisements = document.getElementsByClassName('banner-box')
    if (advertisements.length == 0) {
        advertisements = document.getElementsByClassName('banner-box')
    }

    const url = window.location.href.split('?')[0]
    
    /**
     * Check if ads are in viewport
     */
    const checkItems = () => {

        for (let el of advertisements) {
            if (isInViewport(el) && trigger_elements.includes(el) == false) {
               
                let banner_id = el.getAttribute('banner-id')
                // ping nodejs
                let payload = {
                    url: url,                             
                }
                postToBackend('view', banner_id, payload)
                // array keeps triggered element. probably works better with el.id
                trigger_elements.push(el)
            }
        } 
    }

    const addClickEvent = () => {
        for (let item of advertisements) {
            item.onclick = function () {

                let banner_url = this.getAttribute('banner-url')
                let banner_id = this.getAttribute('banner-id')                
                
                const url = window.location.href.split('?')[0]

                let payload = {
                    url: url,
                    full_url: window.location.href              
                }

                postToBackend('click', banner_id, payload);
                setTimeout(function () {
                    let win = window.open(banner_url, '_blank');
                    win.focus();
                }, 500);
            }
        }
    }

    // add click event to ads boxes    
    addClickEvent()
    // initial state. check if any advertisement is visible.
    checkItems()

    document.addEventListener('scroll', function () {
        // all advertisements were trigger. no need to loop over items again
        if (trigger_elements.length != advertisements.length) {
            checkItems()            
        }
    }, {
        passive: true
    });

}

document.addEventListener('DOMContentLoaded', function () {
    init_ads()
})