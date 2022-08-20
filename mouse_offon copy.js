// http://jscript.zouri.jp/Source/KeybordCtrl.html

//  Shell関連の操作を提供するオブジェクトを取得
var sh = new ActiveXObject( "WScript.Shell" );

//  マウスプロパティを起動
sh.Run("control MAIN.CPL");

//  起動してすぐにキー送信すると失敗する可能性があるので、3秒停止
WScript.Sleep( 100 );

sh.SendKeys ("^{TAB 2}");
sh.SendKeys ("{TAB}");
WScript.Sleep( 100 );
sh.SendKeys ("e");
sh.SendKeys ("{TAB 5}");
WScript.Sleep( 100 );
sh.SendKeys ("{ENTER}");
sh.SendKeys ("%{F4}")