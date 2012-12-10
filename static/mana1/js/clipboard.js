function init() {
                var clip
                clip = new ZeroClipboard.Client();
                clip.setHandCursor( true );
                clip.addEventListener('load', function (client) {
                });
                clip.addEventListener('mouseDown', function (client) {
                        $("#shadowDiv").attr("class", "showDiv");
                        $("#tishi").attr("class", "showTishi");
                        clip.setText2($("#result").table2CSV({separator: '\t',delivery:"value"}));
                });
                clip.addEventListener('complete', function (client, text) {
                        $("#shadowDiv").attr("class", "hidDiv");
                        $("#tishi").attr("class", "hidDiv");
                        if (text.length>0){
                            alert("复制成功")
                        } else{
                            alert("复制失败")
                        }
                });
                clip.glue('io');
}

