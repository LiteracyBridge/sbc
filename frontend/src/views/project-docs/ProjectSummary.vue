<script setup lang="ts">
import { useProjectDataStore } from "@/stores/projectData";
import { useProjectStore } from "@/stores/projects";
import type { Organisation } from "@/types";
import { computed } from "vue";

const props = defineProps<{ organisation: Organisation }>();

const store = useProjectDataStore(),
  projectStore = useProjectStore();

const project = computed(() => projectStore.current_project);
</script>

<template>
  <!-- The header of the content pages is only a line so we have no content here but add the line with our CSS. -->
  <header style="visibility: hidden;"></header>
  <!-- The footer for all content pages contains the link to the website and a line next to it. -->
  <footer class="footerStandard" v-if="organisation.website">
    <a :href="organisation.website">
      {{ organisation.website }}
    </a>
    <hr />
  </footer>

  <!--
    The footer for the bibliography contains more information then the footer pages of the standard pages,
    it contains the website, email and phone number.
-->
  <footer class="footerBibliography">
    <div>
      <a :href="organisation.website" v-if="organisation.website">
        {{ organisation.website }}
      </a>

      <br />
      <a :href="'mailto' + organisation.email" v-if="organisation.email">
        {{ organisation.email }}
      </a>
      <br />
      <!-- <span> 317.123.2345 </span> -->
    </div>
    <hr />
  </footer>

  <!--
    The cover page has a full page background image which we will set via CSS, the book title and a footer
    with the website, email and phone number.
-->
  <div class="coverPage">
    <h1>{{ project.name }}</h1>
    <div class="coverFooter">
      <span>
        <a :href="organisation.website" v-if="organisation.website">
          {{ organisation.website }}
        </a>
        <a :href="'mailto' + organisation.email" v-if="organisation.email">
          {{ organisation.email }}
        </a>
      </span>
      <hr />
    </div>
  </div>
  <!--
    The table of contents contains a sample toc based on <dl> elements and a image at the bottom of the toc.
-->
  <div class="tocPage">
    <h1>Table of Contents</h1>
    <hr />

    <div class="twoColumns">
      <dl>
        <dt>1. Project Information</dt>
        <!-- <dd>Project Information</dd> -->

        <dt>2. Background and Context</dt>

        <dt>3. Project Objectives</dt>

        <dt>4. Audiences</dt>
        <dd></dd>

        <!-- <dt>03</dt>
        <dd>Duis Ornare</dd> -->
      </dl>
      <dl></dl>
    </div>
  </div>

  <!--
    Each chapter of the book is wrapped by a <div> with the .chapterPage class.
    Each chapter has a title <h1> element a line below and then some highlighted text.
    In this chapter we also have light highlighted text (blue but not bold) and a two column text.
-->
  <div class="chapterPage">
    <h1 class="highlight">1 Project Information</h1>
    <hr />

    <!-- <p class="highlight">
      Aenean convallis lorem diam, ut imperdiet lectus ornare eget. Vestibulum consequat
    </p> -->

    <!-- <p class="highlightLight">
      Aenean convallis lorem diam, ut imperdiet lectus ornare eget. Vestibulum consequat
    </p> -->

    <div v-for="(q, count) in store.questionsForTopic('basic')">
      <h4 class="bold">{{ q.q2u }}</h4>

      <p style="margin-bottom: 10px">
        {{ store.getData(q.id) }}
      </p>
    </div>
  </div>

  <div class="chapterPage">
    <h1 class="highlight">2 Background and Context</h1>
    <hr />

    <div v-for="(q, count) in store.questionsForTopic('background')">
      <h4 class="bold">{{ q.q2u }}</h4>

      <p style="margin-bottom: 10px">
        {{ store.getData(q.id) }}
      </p>
    </div>
  </div>

  <div class="chapterPage">
    <h1 class="highlight">3 Project Objectives</h1>
    <hr />

    <div v-for="(q, count) in store.questionsForTopic('objectives')">
      <h4 class="bold">{{ q.q2u }}</h4>

      <p style="margin-bottom: 10px">
        {{ store.getData(q.id) }}
      </p>
    </div>

    <div>
      <h4 class="bold">
        What specific objective(s) will your project achieve? What changes will your
        project make happen?
      </h4>

      <ol style="margin-bottom: 10px; margin-left: 0.5cm">
        <li
          v-for="item in store.new_project_data.filter((p) => p.module == 'objectives')"
        >
          {{ item.data }}
        </li>
      </ol>
    </div>
  </div>

  <div class="chapterPage">
    <h1 class="highlight">4 Audiences</h1>
    <hr />

    <div>
      <h4 class="bold">
        Who is the primary target audience for your project? Who will be adopting the
        behavior you want to influence?
      </h4>

      <ol style="margin-bottom: 10px; margin-left: 0.5cm">
        <li
          v-for="item in store.new_project_data.filter(
            (p) => p.name == 'primary_audience'
          )"
        >
          {{ item.data }}
        </li>
      </ol>
    </div>

    <div>
      <h4 class="bold">Who else influences the actions of your main target audience?</h4>

      <ol style="margin-bottom: 10px; margin-left: 0.5cm">
        <li
          v-for="item in store.new_project_data.filter(
            (p) => p.name == 'secondary_audience'
          )"
        >
          {{ item.data }}
        </li>
      </ol>
    </div>

    <div v-for="(q, count) in store.questionsForTopic('audiences')">
      <h4 class="bold">{{ q.q2u }}</h4>

      <p style="margin-bottom: 10px">
        {{ store.getData(q.id) }}
      </p>
    </div>
  </div>
</template>

<style>
/*
Import the desired font from Google fonts.
*/
@import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap");

/*
Define all colors used in this template
*/
:root {
  --highlight-color-one: #289b6a;
  --highlight-color-one-transparent: #289b6a;
  --text-color: #303e48;
  --table-row-separator-color: #cec3ba;
}

@page {
  /*
  This CSS highlights how page sizes and margin boxes are set.
  https://docraptor.com/documentation/article/1067959-size-dimensions-orientation
  Within the page margin boxes content from running elements is used instead of a
  standard content string. The name which is passed in the element() function can
  be found in the CSS code below in a position property and is defined there by
  the running() function.

  On the bottom right page margin box we also add the current page number and
  in the @footnote rule we define the style of the footnote area.
  */
  size: A4;
  margin: 2cm 2cm 2.5cm 2cm;
  counter-reset: footnote;

  @top-left {
    content: element(header);
  }

  @bottom-left {
    width: 100%;
    content: element(footer);
  }

  @bottom-right {
    font-family: "Montserrat", sans-serif;
    font-size: 8pt;
    font-weight: bold;
    color: var(--highlight-color-one);
    content: counter(page, decimal-leading-zero);
  }

  @footnote {
    border-top: 0.125mm solid var(--table-row-separator-color);
    padding-top: 2mm;
  }
}

/*
The bibliography page has a different HTML element as footer content so instead of
the running element "footer" we add the running element "footerBibliography" here.
*/
@page bibliography {
  @bottom-left {
    width: 100%;
    content: element(footerBibliography);
  }
}

@page: first {
  /*
  This CSS highlights how the margin, background and page margin boxes are set
  only for the first page of the PDF.

  As the first or cover page should not get the header and footer like all other
  pages, we set the content of these page margin boxes to empty.
  */
  margin: 0;
  background-size: cover;
  background-image: url(https://images.unsplash.com/photo-1497250681960-ef046c08a56e?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1834&q=80);

  @top-left {
    content: "";
  }

  @bottom-left {
    content: "";
  }
}

/*
The body itself has no margin or padding.
Additionally the default font family, size and color for the document is defined
here.

Also we define the counter for the chapter numbers here with the property counter-reset.
*/
body {
  margin: 0;
  padding: 0;
  color: var(--text-color);
  font-family: "Montserrat", sans-serif;
  font-size: 10pt;
  counter-reset: chapters;
}

/*
The links in the document should not be highlighted by an different color and underline
instead we use the color value inherit to get the current texts color.
*/
a {
  color: inherit;
  text-decoration: none;
}

/*
Any HR HTML element should get the highlight color.
*/
hr {
  height: 0;
  border: 0;
  border-top: 0.75mm solid var(--highlight-color-one);
  margin: 1cm 0 1cm 0;
}

/*
The page header in our document uses the HTML HEADER element, we define a height
of 2cm and a border on the bottom of half a millimeter.
As mentioned above in the comment for the @page the position property with the
value running(header) makes this HTML element float into the top left page margin
box. This page margin box repeats on every page in case we would have a multi-page
book.
*/
header {
  position: running(header);
  height: 2cm;
  border-bottom: 0.5mm solid var(--table-row-separator-color);
}

/*
Anything after the cover, toc and chapter elements should start on a new page so we do
set a page break of always after these elements.
*/
.coverPage,
.tocPage,
.chapterPage {
  page-break-after: always;
}

/*
For the pageBreak elements we also set a height of 1cm to get some spacing between the header
line and the content.
*/
.pageBreak {
  page-break-before: always;
  height: 1cm;
}

/*
On the cover page the text color needs to be white as we have a background image on the whole
page. Also we set a margin of 2cm.
*/
.coverPage {
  /* color: green; */
  margin: 2cm;
}

/*
The book title should have a margin to the top of 6cm and also a font size of 64pt.
*/
.coverPage h1 {
  margin-top: 6cm;
  font-size: 64pt;
}

/*
The footer on the cover page containing the website, email, phone number and line need
to be on the bottom of the page so we set the position to absolute, bottom 1cm. Also
the items should be aligned in the center so the line is in the vertical center of the text.
*/
.coverPage .coverFooter {
  text-transform: uppercase;
  font-size: 8pt;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: absolute;
  bottom: 1cm;
  width: calc(100% - 4cm);
}

/*
The first link in the cover page footer (the like to the website) should be bold.
*/
.coverPage .coverFooter a:first-of-type {
  font-weight: bold;
}

/*
The line in the footer has a height of 0.5mm and white as a background color.
*/
.coverPage .coverFooter hr {
  height: 0.5mm;
  background-color: white;
  border-top: 0;
  width: 40%;
}

/*
To get another page footer on the bibliography we need to use the page property
and set a unique page name for which we defined a @page rule above.
*/
.bibliographyPage {
  page: bibliography;
}

/*
Most <h1> header elements (except cover page) get a margin top of 1cm and the
text is transformed to uppercase.
*/
.chapterPage h1,
.tocPage h1,
.bibliographyPage h1 {
  margin-top: 1cm;
  text-transform: uppercase;
}

/*
The content chapter pages and the bibliography page get a "chapter" number
before their title. For this we use the chapters counter. The second parameter
in the counter() funtion allows us to add a leading 0 to chapter numbers below
10.
*/
.chapterPage h1::before,
.bibliographyPage h1::before {
  counter-increment: chapters;
  /* content: counter(chapters) " "; */
}

/*
To ensure images do not take too much space you could either take care that the
editors select images in the proper sizing or define a container where you set
a fixed height and hide anything which overflows.
*/
.imageContainer {
  max-height: 9cm;
  overflow: hidden;
}

/*
In the image container all images should have a max width of 100% of the wrapping
element.
*/
.imageContainer img {
  max-width: 100%;
}

/*
In two colums layouts where one colum is a image we also use a container to ensure
a max size, in this case it is dependend on the max height instead of the width.
*/
.imageContainerColumns {
  overflow: hidden;
  max-height: 180mm;
}

/*
In the tow column image container the image should not exceed 100% of the containers
height.
*/
.imageContainerColumns img {
  max-height: 100%;
}

/*
All two and three column content is done via flexbox.
*/
.twoColumns,
.threeColumns {
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  margin: 1cm 0 1cm 0;
}

/*
In two column content each column gets a width of 48% so
we get 4% of space between them.
*/
.twoColumns > * {
  width: 48%;
}

/*
In three column content each column gets a width of 30% so
between the columns we have 3.33% space.
*/
.threeColumns > * {
  width: 30%;
}

/*
If both columns are text only we use this class and simply set
a column gap of 1cm.
*/
.twoTextColumns {
  margin: 1cm 0 1cm 0;
  column-count: 2;
  column-gap: 1cm;
}

/*
The table of contents elements (<dl>) and all highlighted text should
get the color defined in the var --highlight-color-one.
*/
dl,
.highlight,
.highlightLight {
  color: var(--highlight-color-one);
}

/*
Additionally the main highlight text should be bold and larger than the others.
*/
.highlight {
  font-weight: #19191900;
  font-size: 14pt;
}

/*
If a image container is followed by a highlight text there should be a gap of 1cm
between them.
*/
.imageContainer + .highlight {
  margin-top: 1cm;
}

/*
Within the texts we use a lot of <h4> headings and we want them to look the same
as the normal text, except their default bold style. So for that we set the text
size to 10pt and margin to 0 so there is no gap between the <h4> and <p> elements.
*/
h4 {
  font-size: 10pt;
  margin: 0;
}

/*
As mentioned in the h4 class we do not want a gap between the <h4> and <p> elements.
So the margin top is set to 0.
*/
p {
  margin-top: 0;
}

/*
For the table of contents we use <dt> and <dd> elements, this <dt> elements should
be a little larger than the normal text so we set a font size of 16pt.
*/
dt {
  font-size: 16pt;
}

/*
After each table of contents entry we at a 0.5cm gap to the next entry.
*/
dd {
  margin: 0 0 0.5cm 0;
}

/*
All footnote elements are getting the float "footnote" property to remove them
from the normal page flow and add them to the footnote area. The rest ensures
the style of the footnote is the same as the normal text, just a smaller font
size of 8pt.
*/
.footnote {
  float: footnote;
  margin-bottom: 2mm;
  color: var(--text-color);
  font-family: "Montserrat", sans-serif;
  font-size: 8pt;
  font-weight: normal;
  footnote-style-position: inside;
}

/*
For the footer we use flexbox to align the items vertically.
*/
.footerStandard,
.footerBibliography {
  position: running(footer);
  color: var(--highlight-color-one);
  display: flex;
  align-items: center;
  font-size: 8pt;
  text-transform: uppercase;
}

/*
The first link element (website link) in each footer should be bold.
*/
footer a:first-of-type {
  font-weight: bold;
}

/*
This is the style of the line in the footer, we give a fixed height of 0.5mm and
a relative size of 70%, the background color is the content of the CSS var --highlight-color-one.
*/
footer hr {
  margin: 0 3% 0 3%;
  height: 0.5mm;
  background-color: var(--highlight-color-one);
  border-top: 0;
  width: 70%;
  display: inline-block;
}

/*
The only difference between the footer of the chapter pages and the bibliography
is that a different HTML element is used for the running position.
*/
.footerBibliography {
  position: running(footerBibliography);
}

.bold {
  font-weight: bold;
}
</style>
