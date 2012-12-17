function clip() {
    clip = new ZeroClipboard.Client();
    clip.setHandCursor( true );
    clip.addEventListener('load', function (client) {
    });
    clip.addEventListener('mousedown', function (client) {
            //console.log(fm2csv(oTable.fnGetData()).join('\r\n'));
            clip.setText(fm2csv(oTable.fnGetData()).join('\r\n'));
    });
    clip.addEventListener('complete', function (client, text) {
            $("#shadowDiv").attr("class", "hidDiv");
            $("#tishi").attr("class", "hidDiv");
            if (text.length>0){
                alert("复制成功");
            } else{
                alert("复制失败");
            }
    });
    clip.glue('io');
}

function fm2csv(Tabledata){
    result = [];
    if (Tabledata.length > 0){
        for (i in Tabledata) {
            y = [Tabledata[i].join('\t')];
            result.push(y);
        }
    }
    return result
}

function clip2() {
        clip = new ZeroClipboard.Client();
        clip.setHandCursor( true );
        clip.addEventListener('load', function (client) {
        });
        clip.addEventListener('mousedown', function (client) {
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
        clip.glue( 'io' );
}

