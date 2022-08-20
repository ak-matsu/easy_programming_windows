// http://jscript.zouri.jp/Source/KeybordCtrl.html

//  Shell関連の操作を提供するオブジェクトを取得
var sh = new ActiveXObject( "WScript.Shell" );

//  マウスプロパティを起動
sh.Run("control MAIN.CPL");

//  起動してすぐにキー送信すると失敗する可能性があるので、3秒停止
WScript.Sleep( 3000 );

// WshShell.Run("control MAIN.CPL");
// wait("ポインター オプション")
// WshShell.SendKeys ("^"+"{TAB}");
// WshShell.SendKeys ("^{TAB 3}");