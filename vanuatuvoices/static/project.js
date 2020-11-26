VANUATUVOICES = {};

VANUATUVOICES.addResizer = function(map) {
    L.control.resizer({ direction: 's' }).addTo(map.map);
}

VANUATUVOICES.addResizerAndAudioplayer = function(map) {
    VANUATUVOICES.addResizer(map);
    CLLD.AudioPlayer.addToMap(map);
}
