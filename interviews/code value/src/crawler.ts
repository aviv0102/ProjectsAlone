import fs from 'fs'
import { Link } from 'Links';
import { WriteResults } from './utils/resultsManager';

export async function crawlUrls(paths: string[], depth: number, http: boolean): Promise<string[]> {
  const results: Link[] = [];
  const links = [];

  for (const path of paths) {
    const onePageLinks = await crawlOneFile(path, depth);
    links.push(onePageLinks);
    results.push({[path] : onePageLinks })
  }

  await WriteResults(results) // Part 3
  
  return [].concat.apply([], links);
}


async function crawlOneFile(path: string, depth: number): Promise<string[]> {
  const data = await fs.promises.readFile(path, 'utf8');
  const links = await findLinksInData(data, depth);

  return links
}


async function findLinksInData(data: string, depth: number): Promise<string[]> {
  const links = [];
  const tags = getAllTags(data);

  let currentDepth = 0;

  for (const tag of tags) {
    if (tag.startsWith('<a')) {
      currentDepth += 1;

      if (currentDepth <= depth) {
        const link = tag.match(/href="([^\'\"]+)/g);
        links.push(link.toString() + '"')
      }
    }
    if (tag.startsWith('</a')) {
      currentDepth -= 1;

    }
  }

  return links
}


function getAllTags(data: string) {
  let newstr = data.replace(/</gi, "<><");
  return newstr.split("<>").filter(t => t != "");
}

/*
  What is this??

  As an example, the following extracts links from given website URL or file path
  scrapeLinks('htmls/1.html', false).then(console.log);
  scrapeLinks('http://some-website.com/', true).then(console.log);
*/