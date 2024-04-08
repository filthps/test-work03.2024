import {en, Faker, ru, uk} from 'https://esm.sh/@faker-js/faker';
export const USE_BROWSER_FAKER = false
export const USE_API_FAKER = true
export const USE_SUBMIT_AND_PAGE_RELOAD = false
export const CustomFaker = new Faker({
  locale: [ru, en, uk],
})
