import { getHandlers } from './get_handlers';
import { postHandlers } from './post_handlers';

export const restHandlers = [...getHandlers, ...postHandlers];
