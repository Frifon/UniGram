/**
 *
 * Crop Image While Uploading With jQuery
 * 
 * Copyright 2013, Resalat Haque
 * http://www.w3bees.com/
 *
 */

// set info for cropping image using hidden fields
// function setInfo(i, e) {
// 	$('#x').val(e.x1);
// 	$('#y').val(e.y1);
// 	$('#w').val(e.width);
// 	$('#h').val(e.height);
// 	// $('#uploadPreviewSmall').attr('style', 'position:relative;width: ' + e.x1 + 'px;height: ' + e.y1 + 'px;');
// }

$(document).ready(function() {
	var p = $("#uploadPreview");

	// prepare instant preview
	$("#uploadImage").change(function(){

		// alert(p.attr('src')); // $("#uploadPreviewSmall").attr('src', $("#uploadPreview").attr('src'));
		// fadeOut or hide preview
		p.fadeOut();

		// prepare HTML5 FileReader
		var oFReader = new FileReader();
		oFReader.readAsDataURL(document.getElementById("uploadImage").files[0]);

		oFReader.onload = function (oFREvent) {
	   		p.attr('src', oFREvent.target.result).fadeIn();
		};
		// alert(p.attr('src'));

	});

	// implement imgAreaSelect plug in (http://odyniec.net/projects/imgareaselect/)
	// $('img#uploadPreview').imgAreaSelect({
	// 	// set crop ratio (optional)

	// 	aspectRatio: '1:1',
	// 	onSelectEnd: setInfo
	// });
});