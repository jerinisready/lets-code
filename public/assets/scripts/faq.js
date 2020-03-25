(function(){
	document.querySelectorAll('.needs_improvement').forEach(function(node){
		node.addEventListener('click', function(event){
			fetch('/needs-improvement/', {
				credentials:'include', method:'post',
				headers:{'Content-Type': 'application/json'},
				body: JSON.stringify({vote:(event.target.getAttribute('data-status') === 'voted')?:'remove': 'add'}),
			}).then(function (r){
				if(r.ok){
					if( event.target.getAttribute('data-status') === 'voted'){
						event.target.classList.remove('text-success');
						event.target.setAttribute('data-status', '');
					}else{
						event.target.classList.add('text-success');
						event.target.setAttribute('data-status', 'voted');
					}
				}
			})
		})
	})
	document.querySelectorAll('.clip_it').forEach(function(node){
		node.addEventListener('click', function(event){
			fetch('/clip-it/', {
				credentials:'include', method:'post',
				headers:{'Content-Type': 'application/json'},
				body: JSON.stringify({vote:(event.target.getAttribute('data-status') === 'voted')?:'remove': 'add'}),
			}).then(function (r){
				if(r.ok){
					if( event.target.getAttribute('data-status') === 'voted'){
						event.target.classList.remove('text-danger');
						event.target.setAttribute('data-status', '');
					}else{
						event.target.classList.add('text-danger');
						event.target.setAttribute('data-status', 'voted');}
				}
			})
		});
    })
})()
