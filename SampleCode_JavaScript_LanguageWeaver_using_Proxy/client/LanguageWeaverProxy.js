function doTranslation() {
	var text = document.getElementById('inputText').value;
	var src = document.getElementById('inputSource').value;
	var trg = document.getElementById('inputTarget').value;
	$.ajax({
		type: 'GET', 
		url: 'http://localhost:8080/translate/' + b64EncodeUnicode(text) + "/" + src + "/" + trg,
		success: function(data) {
			document.getElementById("labelOutput").innerText = b64DecodeUnicode(data);
		}, error: function (xhr, state, err) {
			alert('failed '+ state + ", " + err + ", " + xhr.responseText );
		}
	});
}

function b64EncodeUnicode(str) {
	return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g,
		function toSolidBytes(match, p1) {
			return String.fromCharCode('0x' + p1);
		}));
}

function b64DecodeUnicode(str) {
	return decodeURIComponent(atob(str).split('').map(function(c) {
		return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
	}).join(''));
}
