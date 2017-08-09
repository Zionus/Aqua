var todayDate = new Date().toISOString().slice(0,10).replace('-','').replace('-','');

function setCode(val){
		return "<a href='https://bz.labs.lenovo.com/show_bug.cgi?id= " + val + "'>" + val + "</a>";
	}

function push(){
	//get a new source and update page
	

    $.ajax({

        //type: "POST",
        url: "/push",
        //data: {t: 3}, beforeSend: function() {},
        success: function(data) {
			myDate = new Date();
			now = myDate.toLocaleString( );
			$('#test').append('<span class="badge">'+now +'</span>');
            }
    });
}
function GetRequest() {
  
  var url = location.search; //获取url中"?"符后的字串
   var theRequest = new Object();
   if (url.indexOf("?") != -1) {
      var str = url.substr(1);
      strs = str.split("&");
      for(var i = 0; i < strs.length; i ++) {
         theRequest[strs[i].split("=")[0]]=(strs[i].split("=")[1]);
      }
   }
   return theRequest;
}
/*

	*/
function gotcha (arg){
	
	$.getJSON( "/gotcha",{name: arg},function  (data){
		labels = data.labels;
		labels.forEach(function(each){
		var label = each;
		//var cols = JSON.stringify(data[label + '_cols']).split(',');
		var cols = eval(data[label + '_cols'])
		//alert(data[label + '_cols']);
		var $table = $("#pv_"+each).bootstrapTable({
				//alert(data.each.length);
				data: data[each]
			});   
			
		$table.on('click', 'tbody > tr > td', function (e){
		var table = $table.data('bootstrap.table'),
			$element = $(this),
			$tr = $element.parent(),
			row = table.data[$tr.data('index')],
			cellIndex = $element[0].cellIndex ,
			$headerCell = table.$header.find('th:eq(' + cellIndex + ')'),
			field = $headerCell.data('field'),
			value = row[field];
		
		table.$el.trigger($.Event('click-cell.bs.table'), [value, row, $element]);
	});

	$table.on('click-cell.bs.table', function(e, value, row, $element){
		/*
		//$element.appendChild()
		//$('#defect-details').modal('show')
		$.getJSON( "/catcha",{name: arg,funz  = row_marker ,label  = col_marker ,tab =  label }, function  (data){
			var $table = $("#target").bootstrapTable({
				//alert(data.each.length);
				data: data['target']
			});   
		}
		*/
		if (value != '')
		{
			var col_marker = cols[$element[0].cellIndex - 3]; //wrong
			row_marker =  JSON.parse(JSON.stringify(row) )['Function'];
			var project =  JSON.parse(JSON.stringify(row) )['Project'];
			var is_all = false
			//alert(project);
			if (project == 'All'){
				is_all = true
						}
			$.getJSON( "/catcha",{name: arg,funz : row_marker ,label: col_marker ,tab :label, is_all :is_all }, function  (data)
				{
					$('#target').bootstrapTable("destroy");
					var $tab = $("#target").bootstrapTable({
						//alert(data['target'].length);
						data: data['target']
					});   
				});
			$('#defect-details').modal('show');
			//alert(row_marker   + ' : ' + col_marker + '  in ' + label );
			
		}

			
		});
	});	
	});
		$('#sourcelist').find("a").attr({"href" :'static/downloads/' + arg + '/' + todayDate + '_pv.csv' });
		$('#sourcelist').find("a").html( arg  + '_source');
		//<a href=" static/downloads/' + arg + '/' + todayDate + '_pv.csv' + '" >' +  arg  + '_source</a>');	
		    
	

}
function setLink(val){
	//return "<a href='#'>" + val + "</a>";
	
	return "<a href='#'>" + val + "</a>";
}
function closer(){
	$('#defect-details').on('shown', function () {
      $('#defect-details').modal('hide');
})
}


$(function () {
	today = new Date();
	nowStr = today.getFullYear() + "/"+ (today.getMonth()+1) + "/" + today.getDay()  + " ["+
	today.getHours() + ":"+ today.getMinutes() + ":"+ today.getSeconds() + "]."+ "&times";
	foreword = $('#nowing').text();
	//alert(foreword);
	$('#nowing').text(foreword + nowStr);
	
			var Request = new Object();
		Request = GetRequest();
		arg= Request['name'];
	gotcha (arg);
	$('#refresh').bind('click',function(){
	$.getJSON( "/gotcha",{name: arg},function  (data){
	labels = data.labels;
	labels.forEach(function(each){
		var label = "#pv_"+each
		//alert(label);
		$(label ).bootstrapTable({
			//alert(data.each.length);
			data: data[each]
		}); 

	
	
		});	
		//<a href="{{ url_for('static', filename='downloads/'+ name + '/20170612_pv.csv' )}}">{{ name }} + source</a>
});
	
	});
	
	setTimeout(function () {
	push();
		},1000);	
/*set interval for update source as 300000*/
setInterval(function() {
		push();
		},
		300000);
		

});



/* only if I had celery
 function start_long_task() {
        // add task status elements 
        div = $('<div class="progress"><div></div><div>0%</div><div>...</div><div>&nbsp;</div></div><hr>');
        $('#progress').append(div);

        // create a progress bar
        var nanobar = new Nanobar({
            bg: '#44f',
            target: div[0].childNodes[0]
        });

        // send ajax POST request to start background job
        $.ajax({
            type: 'POST',
            url: '/longtask',
            success: function(data, status, request) {
                status_url = request.getResponseHeader('Location');
                update_progress(status_url, nanobar, div[0]);
            },
            error: function() {
                alert('Unexpected error');
            }
        });
    }

function update_progress(status_url, nanobar, status_div) {
        // send GET request to status URL
        $.getJSON(status_url, function(data) {
            // update UI
            percent = parseInt(data['current'] * 100 / data['total']);
            nanobar.go(percent);
            $(status_div.childNodes[1]).text(percent + '%');
            $(status_div.childNodes[2]).text(data['status']);
            if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS') {
                if ('result' in data) {
                    // show result
                    $(status_div.childNodes[3]).text('Result: ' + data['result']);
                }
                else {
                    // something unexpected happened
                    $(status_div.childNodes[3]).text('Result: ' + data['state']);
                }
            }
            else {
                // rerun in 2 seconds
                setTimeout(function() {
                    update_progress(status_url, nanobar, status_div);
                }, 2000);
            }
        });
    }
*/	
