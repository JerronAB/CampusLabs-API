let SLOs = {'Livestock Species':['AGR 240','AGR 280']}
var links = document.getElementsByTagName('a')

Object.keys(SLOs).forEach(Current_SLO => {
	for(var i = 0; i < links.length; i++) {
		var link = links[i];
		console.log(links[i]);
		if (link.innerHTML.includes(Current_SLO)) {
			link.click()
			for (const course in SLOs[Current_SLO]) {
				var how_is_assmnt_prfmed = document.getElementsByClassName('measures__large-button')
				index = 0
				while (document.getElementsByClassName('measures__large-button').length == 0 && index < 60000) {
					console.log("Waiting for objects to appear. ");
					console.log(index)
					console.log(document.getElementsByClassName('measures__large-button').length)
					//how_is_assmnt_prfmed = document.getElementsByClassName('measures__large-button'); 
					index += 1;}
				for(var i = 0; i < 3; i++) {
					if (how_is_assmnt_prfmed[i].innerHTML.includes("Connection")) {how_is_assmnt_prfmed[i].click();break;}
					}
				connection_type = document.getElementsByClassName('btn btn-default')
				for(var i = 0; i < 9; i++) {
					if (connection_type[i].innerHTML.includes("Assign")) {connection_type[i].click();break;}
					}
				}
			break;	
			}
			}
		}
);