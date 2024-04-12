import { getHandlers } from './get_handlers';
import { postHandlers } from './post_handlers';
import { deleteHandlers } from './delete_handlers';

export const restHandlers = [...getHandlers, ...postHandlers, ...deleteHandlers];
