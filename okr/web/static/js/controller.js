
function sortByProperty(property){  
  return function(a,b){  
     if(a[property] > b[property])  
        return 1;  
     else if(a[property] < b[property])  
        return -1;  
 
     return 0;  
  }  
}

function create(apiResult) {
    // const apiResult = [{
    //     title: "title1",
    //     description: "desc1",
    //     output: "out1"
    //   }, {
    //     title: "title2",
    //     description: "desc2",
    //     output: "out2"
    //   }, {
    //     title: "title3",
    //     description: "desc3",
    //     output: "out3"
    //   }];
    
      const container = document.getElementById('accordion');

      
      apiResult.forEach((result, idx) => {
        // Create card element
        const card = document.createElement('div');
        card.classList = 'card-body';
      
        // Construct card content
        
        var content = `
            <li class="accordion-item">
              <div class="card-bd">
          `;
          // TODO: iterate apiResult highlights and generate card in highlight time order
          var red_highlights = result["red"];
          var yellow_highlights = result["yellow"];
          var yellow_and_blue_highlights = result["cyan"].concat(yellow_highlights);
          yellow_and_blue_highlights = yellow_and_blue_highlights.sort(sortByProperty("date"));
          red_highlights.forEach((rh, idx) => {
            content += `<a style="font-size: 120%; margin-top: 0; margin-bottom: 0px; color: black; overflow-wrap: break-word;" href=${result.url} target="_blank">${rh.text}</a></br>`;
          })
          content += `<a style="font-size: 80%; margin-bottom: 0.5rem; overflow-wrap: break-word;" href=${result.url} target="_blank">${result.url}</a>
                      <div class="card-contnt">`
          yellow_and_blue_highlights.forEach((result, idx) => {
            if (result.className == "yellow") { 
              content += `<p style="background-color: rgba(255, 255, 170, 0.8); margin-bottom: 0.5rem; overflow-wrap: break-word;">${result.text}</p>`;
            } else {
              content += `<p style="background-color: rgba(170, 255, 255, 0.8); margin-bottom: 0.5rem; overflow-wrap: break-word;">${result.text}</p>`;
            }
          })
          content += ` 
                </div>
              </div>
            </li>`;
      
        // Append newyly created card element to the container
        container.innerHTML += content;
      })

}


function destroy() {
    const container = document.getElementById('accordion');
    container.innerHTML = '';
}


function query() {
    document.getElementById("search-button").focus();
    destroy()
    let searchText = document.getElementById("search-text").value;
    const json = {
      "search": searchText,
      "user": "blake"
    };
    console.log(JSON.stringify(json))
    let request = new XMLHttpRequest();
    request.open("POST", "http://192.168.86.50:5000/search");
    request.setRequestHeader('Content-Type', 'application/json');
    request.send(JSON.stringify(json));
    request.onload = () => {
      console.log(request)
      if (request.status == 200) {
        console.log(request.response);
        var apiResult = JSON.parse(request.response)
        create(apiResult)
      } else {
        console.log(`error ${request.status} ${request.statusText}`)
      }
    }
}