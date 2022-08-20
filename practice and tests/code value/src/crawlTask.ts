import { crawlUrls } from './crawler';
import { Depth } from './config/config';

export async function crawl(paths: string[], http: boolean) {
  const links = await crawlUrls(paths, Depth, http);
  console.log('links:', links);
}

crawl(['htmls/1.html'], false) // I changed html 1 a bit to have 3 different depths so try it in package.json ...
crawl(['htmls/2.html', 'htmls/3.html'], false);


