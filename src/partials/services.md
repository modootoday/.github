{{> components/section-heading name="sec-services"}}

<p align="center">
{{#each services}}{{> components/card-link href=this.url name=this.card.svg width="49%"}}
{{/each}}</p>
