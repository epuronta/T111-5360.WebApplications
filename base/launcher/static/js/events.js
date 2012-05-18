// JAVASCRIPT FOR THE EVENTS SUBPAGE. ALSO THE LAUNCHER PAGE USES SOME OF THESE FUNCTIONS.

// function to fetch all future Aalto and AYY events (calls displayEvents)
function getEvents(limit) {
	$.ajax({
		url: "/api/events/?limit=999999&offset=0",
		type: "GET",
		dataType: "json",
		success: function(data) {
			if(!data.events) {
				console.log("Error, no events in data", data)
				return;
			}
			data.events.sort(compareDatesFunction);
			displayEvents(data.events, limit);
		}, 
		error: function(jqXHR, textStatus, errorThrown) {
			$('#loading').remove();
			console.log(jqXHR, textStatus, errorThrown);
		}
	});
}

// function to handle and display the events data
function displayEvents(events, limit) {
	var how_many = limit;
	
	var weekday=new Array(7);
	weekday[0]="Sunday";
	weekday[1]="Monday";
	weekday[2]="Tuesday";
	weekday[3]="Wednesday";
	weekday[4]="Thursday";
	weekday[5]="Friday";
	weekday[6]="Saturday";
	
	var month=new Array(12);
	month[0]="January";
	month[1]="February";
	month[2]="March";
	month[3]="April";
	month[4]="May";
	month[5]="June";
	month[6]="July";
	month[7]="August";
	month[8]="September";
	month[9]="October";
	month[10]="November";
	month[11]="December";
	
	// loop through all the events
	for(var i = 0; i < events.length; i++) {
		event = events[i];
		var divider = ""; // day divider <li> tag
		var start_date = createDate(event.start_date);
		// if this events start on a different day than the previous one, create a divider
		if(i == 0 || compareDates(event, events[i-1])) {
			divider = $("<li />")
				.addClass("ui-li-divider")
				.attr({"data-role":"list-divider","role":"heading"})
				.text(weekday[start_date.getDay()] + " " + start_date.getDate() + "." + (start_date.getMonth()+1))
		}
		
		title = formatTitle(event.title); // format the title data
		start_time = formatTime(start_date.getHours()); // format event start time
		
		// create event li tag with its title
		var container = $("<li />")
			.addClass("popup")
			.append(
				$("<a />")
					.attr({"data-role":"button"})
					.append(
						$("<span />")
							.attr("style","color:#CC3300")
							.text(start_time)
					)
					.append(
						$("<span />").text(" " + title)
				)
			);
		
		// set event icon
		var icon = "false"
		event.remote_source_name == "AaltoEvents" ? icon = "evt-icon-aalto" : icon = "evt-icon-ayy";
		
		// set the event its data
		for(prop in event) {
			container
				.attr({"data-theme":"c","data-icon":icon,"data-iconpos":"left"})
				.append(
					$("<span />")
						.addClass(prop)
						.addClass("property")
						.addClass("hidden")
						.html(event[prop])
					);
		}
		
		
		var today = new Date();
		today = new Date(today.getFullYear(), today.getMonth(),today.getDate(),0,0,0,0);
		
		// if no start time has been defined, set it to 18 to avoid tagging the event as a past event
		if(start_date.getHours() == 0) start_date = new Date(start_date.getFullYear(), start_date.getMonth(),start_date.getDate(),18,0,0,0);
		
		// hide the past events/dividers (some date time comparison)
		if(compareDatesString(today, start_date) >= 0) {
			if(divider != "") divider.addClass("past");
			container.addClass("past");
		}
		else {
			how_many > 0 ? container.addClass("visible") : container.addClass("hidden")
			if(how_many <= 0 && divider != "") divider.addClass("hidden");
			how_many -= 1;
		}
		
		// append the data to content div
		$("div[data-role='content']").children("ul").hide().append(divider).append(container);
	}
	
	// append the event filters to the page (Aalto & AYY filter icons on the top right)
	var event_filter = $("<div />")
		.addClass("filters")
		.append(
			$("<div />")
				.css({"width":"32px"})
				.attr("id","AaltoEvents")
				.addClass("filter active")
		)
		.append(
			$("<div />")
				.css({"width":"32px"})
				.attr("id","ayy")
				.addClass("filter active")
		);
	$('.ui-listview-filter').append(event_filter);
	
	// set the styling and css classes for the search bar
	$("div[data-role='content']").children('form').attr("id","scrollable").css({"width":$("#tabs").outerWidth() + "!important"});
	// refresch the view (apply jQuery CSS styling to the new dynamically appeneded content
	$('#eventlist').listview('refresh');
	// remove the loader.gif
	$('#loading').remove();
	// fade the page in
	$("div[data-role='content']").children('ul').fadeIn("slow");
}

// 3 DIFFERENT FUNCTIONS TO MAKE EVENT DATE COMPARISONS (SAME LOGICAL, DIFFERENT INPUT HANDLING)
function compareDatesFunction(evt1, evt2) {
	d1 = createDate(evt1.start_date);
	d2 = createDate(evt2.start_date);
	d1 = new Date(d1.getFullYear(), d1.getMonth(), d1.getDate(),d1.getHours(),0,0,0);
	d2 = new Date(d2.getFullYear(), d2.getMonth(), d2.getDate(),d2.getHours(),0,0,0);
	var one_day=1000*60*60*24;
	return d1.getTime()-d2.getTime();
}

function compareDates(evt1, evt2) {
	d1 = createDate(evt1.start_date);
	d2 = createDate(evt2.start_date);
	d1 = new Date(d1.getFullYear(), d1.getMonth(), d1.getDate(),0,0,0,0);
	d2 = new Date(d2.getFullYear(), d2.getMonth(), d2.getDate(),0,0,0,0);
	var one_day=1000*60*60*24;
	return Math.ceil(d1.getTime()/(one_day))-Math.ceil(d2.getTime()/(one_day));
}

function compareDatesString(d1, d2) {
	if(!is('Date',d1)) {
		d1 = createDate(d1);
		d1 = new Date(d1.getFullYear(), d1.getMonth(), d1.getDate(),0,0,0,0);
	}
	if(!is('Date',d2)) {
		d2 = createDate(d2);
		d2 = new Date(d2.getFullYear(), d2.getMonth(), d2.getDate(),0,0,0,0);
	}
	var one_day=1000*60*60*24;
	return Math.ceil(d1.getTime()/(one_day))-Math.ceil(d2.getTime()/(one_day));
}

// create a date from a string in a date-like format
function createDate(str) {
	regex = /(\d{4})-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d)/;
	date = regex.exec(str)
	return new Date(parseInt(date[1],10), parseInt(date[2],10)-1, parseInt(date[3],10), parseInt(date[4],10), parseInt(date[5],10), parseInt(date[6],10), 0);
}

function getDaysTillEvent(event_date) {
	var today = new Date();
	today = new Date(today.getFullYear(), today.getMonth(),today.getDate(),18,0,0,0);
	// workaround for events that start at 00:00:00 (typically full day events. Lets set the clock time to 18:00:00)
	var temp = new Date(event_date.getFullYear(), event_date.getMonth(), event_date.getDate(),18,0,0,0);
	
	var days_left = compareDatesString(temp, today);
	if(days_left < 0)
		return "past"
	else if(days_left == 0)
		return "today"
	else if(days_left == 1)
		return "tomorrow"
	else
		return days_left + " days"
}

function formatTitle(title) {
	regex = /(\d{2}\.\d{2}\.\d{4}: )?(.+[^( \( \d.\d.\d{4} \))])/;
	title = regex.exec(title)
	return title[2]
}

function formatTime(time) {
	if(!time) return ""
	time += ":00";
	if(time.length == 4) time = "0" + time;
	return time
}

// move the search bar according to the user's scrolling
function scrolling() {
	var form_width = $("#tabs").outerWidth();
	var y0 = $(window).scrollTop();
	if(y0 > 120)
		$("#scrollable").stop().css({"position":"fixed","top":"15px"}).css({"width":form_width});
	else 
		$("#scrollable").stop().css({"position":"relative","top":"0px"}).css({"width":form_width});
}


//testing data types accurately in JavaScript (opposed to "typeof")
//from http://bonsaiden.github.com/JavaScript-Garden/

function is(type, obj) {
	var clas = Object.prototype.toString.call(obj).slice(8, -1);
	return obj !== undefined && obj !== null && clas === type;
}
	

/* For a given date, get the ISO week number
 *
 * Based on information at:
 *
 *    http://www.merlyn.demon.co.uk/weekcalc.htm#WNR
 *
 * Algorithm is to find nearest thursday, it's year
 * is the year of the week number. Then get weeks
 * between that date and the first day of that year.
 *
 * Note that dates in one year can be weeks of previous
 * or next year, overlap is up to 3 days.
 *
 * e.g. 2014/12/29 is Monday in week  1 of 2015
 *      2012/1/1   is Sunday in week 52 of 2011
 */
function getWeekNumber(d) {
	// Copy date so don't modify original
	d = new Date(d);
	d.setHours(0,0,0);
	// Set to nearest Thursday: current date + 4 - current day number
	// Make Sunday's day number 7
	d.setDate(d.getDate() + 4 - (d.getDay()||7));
	// Get first day of year
	var yearStart = new Date(d.getFullYear(),0,1);
	// Calculate full weeks to nearest Thursday
	var weekNo = Math.ceil(( ( (d - yearStart) / 86400000) + 1)/7)
	// Return array of year and week number
	return weekNo;
}

function addScrollEffect() {
	//window.onscroll = function() { scrolling(); };
	document.addEventListener("scroll", scrolling, false);
	document.addEventListener("touchmove", scrolling, false);
	console.log("Add scroll listener");
	return false;	
}

function removeScrollEffect() {
	document.removeEventListener("scroll", scrolling, false);
	document.removeEventListener("touchmove", scrolling, false);
	console.log("Remove scroll listener");
	return false;	
}

// filter logic. Attach the click/tap event to the filters to hide the events (of the respective filter)
$(".filter").live("tap","click", function() {
	var event_src = $(this);
	if(event_src.hasClass("active")) {
		event_src.removeClass("active");
		event_src.addClass("inactive");
	}
	else {
		event_src.addClass("active");
		event_src.removeClass("inactive");
	}
	$('#eventlist').children('li').each(function() {
		var current_event = $(this);
		if(current_event.find('span.remote_source_name').text().toLowerCase() == event_src.attr("id").toLowerCase()) {
			if(event_src.hasClass("active"))
				current_event.removeClass("hidden").addClass("visible");
			else
				current_event.removeClass("visible").addClass("hidden");
		}
	});
});

// add the search bar scroll effect when the user closes an event popup
$('a[rel="close"]').live("click", function() {
	addScrollEffect();
	return false;
});

// get the event data from the AJAXed HTML data and append it to the event popup when an event is clicked
$(".popup").live("tap", "click", function() {
	var descr = $(this).find("span.descr").clone();
	var title = $(this).find("span.title").text();
	var remote_url = $(this).find("span.remote_url").text();
	var start_date = createDate($(this).find("span.start_date").text());
	var days_left = getDaysTillEvent(start_date);
	
	// setting up the google maps hyperlink for the event
	var lat = $(this).find("span.lat").text();
	var lon = $(this).find("span.lon").text();
	var google_maps_str = "http://maps.google.com/maps?q=" + lat + "," + lon + "&amp;ie=UTF8&amp;t=m&amp;z=14&amp;ll=" + lat + "," + lon + "&amp;output=embed";
	var venue = $(this).find("span.venue");
	var venue_text = venue.text()
	venue.length > 0 ? venue_text = venue_text + " @ Google Maps" : venue_text = "@ Google Maps";
	
	// adding the target="_blank" for the anchor tags (external URL references)
	// removing all the empty children elements (except of course img elements)
	$(descr).children().each(function() {
		$(this).removeClass();
		if(!$(this).find('a').attr('target'))
			!$(this).find('a').attr('target','_blank');
		if(!$(this).is("img") && $.trim($(this).text()).length == 0)
			$(this).remove();
	});
	
	// setting up the content div, which is then appended to the popup dialog (down below)
	var content = $("<div />")
		.append(
			$("<h5 />")
				.addClass("remote_url")
				.append(
					$("<a />")
						.attr({"href": remote_url, "target":"blank"})
						.text(formatTitle(title))
				)
		)
		.append(
			$("<span />")
				.append(descr.children())
		)
		.append(
			$("<a />")
				.attr({"rel":"close","data-role":"button","href":"#"})
				.text("Close")
		)
		
	if(lat != 0) {
		content.find("span").after(
			$("<a />")
				.attr({"id":"google_maps","href":google_maps_str,"target":"_blank"})
				.text(venue_text)
		)
	}
	
	// using the easy-to-use simpledialog2 plugin for the popup
	$('<div>').simpledialog2({
		mode : 'blank',
		top : 0,
		headerText : start_date.getDate() + "." + (start_date.getMonth()+1) + ". @ " + formatTime(start_date.getHours()) + " (" + days_left +")",
		headerClose : true,
		blankContent : content.children(),
		callbackOpen : removeScrollEffect() // remove the search bar scrolling effect when an event popup is opened
	});
});