
function display() {
    document.getElementById("demo").innerHTML = "Button Clicked";
}

function displayText() {
    document.getElementById("demo").innerHTML = "Enter The Text";
}

function displayDate(x) {
	if (x<=10){
		document.getElementById("demo").innerHTML = Math.floor(Math.random()*10);
	}else if(x<=100){
		document.getElementById("demo").innerHTML = Math.floor(Math.random()*100);
	}else{
		document.getElementById("demo").innerHTML = Math.floor(Math.random()*1000);

	}
    
}


function dayName(x) {
	var day;
	switch (x) {
	    case 0:
	        day = "Sunday";
	        break;
	    case 1:
	        day = "Monday";
	        break;
	    case 2:
	        day = "Tuesday";
	        break;
	    case 3:
	        day = "Wednesday";
	        break;
	    case 4:
	        day = "Thursday";
	        break;
	    case 5:
	        day = "Friday";
	        break;
	    case  6:
	        day = "Saturday";
	}
document.getElementById("demo").innerHTML = "Today is " + day;

}

function looping() {
	var txt = "";
	var numbers =  [1,2,3,4,5];
	numbers.forEach(myFunction);

	document.getElementById("demo").innerHTML = "ForEach method =" + txt;

	function myFunction(value) {
	    txt = txt+value + 2 +","; 
	    return 
	}
}
function loopingin() {
	var n1 = [45, 4, 9, 16, 25];
	var n2 = n1.map(myFunction);

	document.getElementById("demos").innerHTML ="input" + n1 +"<br>" + "map method =" + n2;

	function myFunction(value) {
	    return value * 2;
	}
    
}
function fill(){
	var numbers = [45, 4, 9, 16, 25];
	var over18 = numbers.filter(myFunction);
	document.getElementById("demos").innerHTML ="input" + numbers +"<br>" + "Filter method(numbers > 18) =" + over18;
	function myFunction(value) {
	    return value > 18;
	}
}


function red(){
	var numbers1 = [1,2,3,4,5];
	var sum = numbers1.reduce(myFunction);
	document.getElementById("demos").innerHTML ="input" + numbers1 +"<br>" + "Reduce Sum = " + sum;

	function myFunction(total, value, index, array) {
	    return total + value;
	}
}


function showCoords(event) {
	// click position
	var content1 = "<ul><li>1</li><li>2</li><li>3</li><li>4</li><li>5</li></ul>"
	var content2 = "<ul><li>6</li><li>7</li><li>8</li><li>9</li><li>10</li></ul>"
    var x = event.clientX;
    var y = event.clientY;
    var posi = document.getElementById("posi");
    var base1 = document.getElementById("class-base");
    var base2 = document.getElementById("class-base2");
    var demo = document.getElementById("demo");
    var demos = document.getElementById("demos");
    // height & width of base1 and base2
    var base1Height = base1.offsetHeight;
    var base1Width = base1.offsetWidth;
    var base2Height = base2.offsetHeight;
    var base2Width = base2.offsetWidth;
    // height & width of demo
    var demoHeigth = demo.offsetHeight;
    var demoWidth = demo.offsetWidth;
    // height & width of demos
    var demosHeigth = demos.offsetHeight;
    var demosWidth = demos.offsetWidth;
    var arrowdown = "&#x25BC;";
    var arrowup = "&#x25B2;";
    var location1 = content1;
    var location2 = content2;
    if(x < base1Width-demoWidth && y < base1Height -demoHeigth){
    	demo.style.display = "block";
   		demo.style.left = x +"px";
   		demo.style.top = y +"px";
        demo.style.textAlign = "left";
    	demo.innerHTML =  arrowdown + location1;
    }else if(x < base1Width && x > base1Width-demoWidth && y < base1Height -demoHeigth){
        x -= demoWidth
        demo.style.display = "block";
        demo.style.left = x +"px";
        demo.style.top = y +"px";
        demo.style.textAlign = "right";
        demo.innerHTML =  arrowdown + location1;
    }else if(x < base1Width-demoWidth && y > base1Height -demoHeigth ){
    	y -= demoHeigth
    	demo.style.display = "block";
    	demo.style.left = x +"px";
   		demo.style.top = y +"px";
        demo.style.textAlign = "left";
    	demo.innerHTML = location1 + arrowup;
    }else if(x < base1Width  && x > base1Width-demoWidth && y > base1Height -demoHeigth ){
        y -= demoHeigth
        x -=demoWidth
        demo.style.display = "block";
        demo.style.left = x +"px";
        demo.style.top = y +"px";
        demo.style.textAlign = "right";
        demo.innerHTML = location1 + arrowup;
    }else if(x > base1Width && x < (base1Width + base2Width - demosWidth) && y < base2Height -demosHeigth){
    	demos.style.display = "block";
    	demos.style.left = x +"px";
   		demos.style.top = y +"px";
        demos.style.textAlign = "left";
    	demos.innerHTML =arrowdown + location2;

    }else if(x > (base1Width + base2Width - demosWidth)&& y < base2Height -demosHeigth){
    	x -= demosWidth
    	demos.style.display = "block";
    	demos.style.left = x +"px";
   		demos.style.top = y +"px";
        demos.style.textAlign = "right";
    	demos.innerHTML =  arrowdown + location2;
    
    }else if(x > base1Width && x < (base1Width + base2Width - demosWidth) && y > base2Height -demosHeigth){
        y-= demosHeigth
        demos.style.display = "block";
        demos.style.left = x +"px";
        demos.style.top = y +"px";
        demos.style.textAlign = "left";
        demos.innerHTML =location2 + arrowup;
    
    }else if(x > (base1Width + base2Width - demosWidth)&& y > base2Height -demosHeigth){
        y -= demosHeigth
        x -=demosWidth
        demos.style.display = "block";
        demos.style.left = x +"px";
        demos.style.top = y +"px";
        demos.style.textAlign = "right";
        demos.innerHTML = location2 + arrowup;
}

}
    // if(y < base1Height -demoHeigth){
    // 	demo.style.display = "block";
   	// 	demo.style.left = x +"px";
   	// 	demo.style.top = y +"px";
    // 	demo.innerHTML = location1;
    // }else if(y > base1Height -demoHeigth){
    // 	y -= demoHeigth
    // 	demo.style.display = "block";
    // 	demo.style.left = x +"px";
   	// 	demo.style.top = y +"px";
    // 	demo.innerHTML = location1;
    // }else if(y < base2Height -demosHeigth){
    // 	demos.style.display = "block";
   	// 	demos.style.left = x +"px";
   	// 	demos.style.top = y +"px";
    // 	demos.innerHTML = location2;
    // }else if(y > base2Height -demosHeigth){
    // 	y -= demosHeigth
    // 	demos.style.display = "block";
    // 	demos.style.left = x +"px";
   	// 	demos.style.top = y +"px";
    // 	demos.innerHTML = location2;
    // }

function cloze1(){
    var demo = document.getElementById("demo");
    demo.style.display ="none"
}
function cloze2(){
    var demos = document.getElementById("demos");
    demos.style.display ="none"
}