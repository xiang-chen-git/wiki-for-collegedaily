/* Add here all your JS customizations */
(function(){	
// Write your own JS functions here.

}());

function increment(event){

		var id = $(this).attr('id');

		var votes = parseInt($(this).attr('data'));
		
		var entry_id = 1;//用的时候comment掉

		var map1 = {'up':'<span class="icon-plus color-blue"></span>', 
					'down':'<span class="icon-minus color-blue"></span>'};
		var map2 = {'up':'靠谱', 
					'down':'不靠谱'};	
		//$.get("/wiki/vote/", {type: id, entry: entry_id}, function(result){
				$(this).html(map1[id]+' '+(votes+1)+' '+ map2[id]);
		//});
	}

function vote(event, entry){
		var id = $(this).attr('id');
		if (id == 'up'){
			$.get(
				'/wiki/vote_up/'+entry+'/',
				{},
				function(data){
					//alert('success');
				}
			)
		}
		else{
			$.get(
				'/wiki/vote_down/'+entry+'/',
				{},
				function(data){
					//alert('success');
				}
			)
		}
	}