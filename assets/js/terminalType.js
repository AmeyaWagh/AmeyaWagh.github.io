
// var typed = new Typed('.element', {
// stringsElement: '#typed-strings'
// });

document.addEventListener('DOMContentLoaded', function(){
	Typed.new('.element', {
	  strings: ["First sentence.", "Second sentence."],
	  typeSpeed: 30
	});
});