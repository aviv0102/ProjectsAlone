import fs from 'fs';
import axios from 'axios';
import url from 'url';
import cheerio from 'cheerio';

const fsPromisified = fs.promises;

function log(p) {
  console.log(p);
}

function fetchUrl(siteUrl) {
  log(`Downloading: ${siteUrl}`);

  const promise = axios.get(siteUrl).then(r => r.data);
  promise.then(() => log(`Download completed: ${siteUrl}`))

  return promise;
}

export async function scrapeLinks(pathUrl: string, http: boolean): Promise<string[]> {
  const html = await (http ? fetchUrl(pathUrl) : fsPromisified.readFile(pathUrl));
  const $ = cheerio.load(html);

  let baseHref = $('base').attr('href');
  if (!baseHref) baseHref = pathUrl;

  return $('a').toArray()
  .map(el => {
    const href = el.attribs.href;
    return !!href ? url.resolve(baseHref, href) : null;
  })
  .filter(o => !!o);
}
