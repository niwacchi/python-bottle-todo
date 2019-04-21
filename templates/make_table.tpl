<p>The Open items are as follows:</p>
<div>
  <table border="1">
    %for row in rows:
    <tr>
      %for col in row:
      <td>{{col}}</td>
      %end
    </tr>
    %end
  </table>
</div>
<div>
  <a href="/new">Add task</a>
</div>