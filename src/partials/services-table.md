<table width="100%">
<tr><th width="20%" align="left">서비스</th><th width="18%" align="left">대상</th><th width="37%" align="left">한 줄 소개</th><th width="25%" align="left">링크</th></tr>
{{#each services}}<tr><td>{{ this.name }}</td><td>{{ this.audience }}</td><td>{{ this.one_line }}<br><sub>{{ this.card.meta }}</sub></td><td>{{#if this.link.site}}<a href="{{ this.link.site }}" title="{{ this.name }} 웹사이트">웹사이트</a><br>{{/if}}{{#if this.link.code}}<a href="{{ this.link.code }}" title="{{ this.name }} 저장소">저장소</a><br>{{/if}}<sub>{{ this.link.label }}</sub></td></tr>
{{/each}}</table>
