{{> components/section-heading name="sec-contact"}}

<p align="center">
{{#each contact}}{{> components/card-link href=this.href name=this.svg width="32%"}}
{{/each}}</p>
<!-- 나중에 추가할 자리: src/data/site.json 의 contact_later 항목(블로그·뉴스레터)을 contact 로 옮기면 카드가 생깁니다.
{{#each contact_later}}{{ this.alt }}: {{ this.href }} ({{ this.svg }})
{{/each}}-->

{{> partials/packages}}

문의 <a href="mailto:support@modoo.today">support@modoo.today</a> · GitHub <a href="https://github.com/modootoday">@modootoday</a> · <a href="https://github.com/myso-kr">@myso-kr</a> · X <a href="https://x.com/datalab_tools">x.com/datalab_tools</a>
