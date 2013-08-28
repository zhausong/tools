<?php
$host='localhost';
$user_name='root';
$password='7256958';

$conn=mysql_connect($host,$user_name,$password);
if (!$conn)
{
    die('数据库连接失败：'.mysql_error());
}
echo '数据库连接成功！';

if (mysql_close($conn))
{
    echo '<br/>...<br/>';
    echo '到数据库的连接已经成功关闭';
}
?>
