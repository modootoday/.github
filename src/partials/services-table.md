<table width="100%">
<tr><th width="20%" align="left">서비스</th><th width="18%" align="left">대상</th><th width="37%" align="left">한 줄 소개</th><th width="25%" align="left">시작하기</th></tr>
{{#each services}}<tr><td>{{ this.name }}</td><td>{{ this.audience }}</td><td>{{ this.one_line }}<br><sub>{{ this.card.meta }}</sub></td><td><a href="{{ this.url }}">{{ this.card.cta }}: {{ this.url_label }}</a>{{#if this.repo}} · <a href="{{ this.repo }}">{{ this.name }} 저장소</a>{{/if}}</td></tr>
{{/each}}</table>
