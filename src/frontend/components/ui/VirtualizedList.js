/**
 * Virtualized list component for handling large datasets efficiently
 */

import { useMemo, useCallback, useRef, useEffect } from 'react';
import { FixedSizeList as List } from 'react-window';

// Memoized list item component
const ListItem = memo(({ index, style, data }) => {
  const { items, renderItem } = data;
  const item = items[index];
  
  return (
    <div style={style}>
      {renderItem(item, index)}
    </div>
  );
});

ListItem.displayName = 'ListItem';

export default function VirtualizedList({
  items = [],
  itemHeight = 50,
  height = 400,
  width = '100%',
  renderItem,
  overscanCount = 5,
  className = '',
  ...props
}) {
  // Memoize item data to prevent unnecessary re-renders
  const itemData = useMemo(() => ({
    items,
    renderItem,
  }), [items, renderItem]);

  // Handle scroll events with throttling
  const handleScroll = useCallback(
    throttle(({ scrollOffset, scrollDirection }) => {
      // Handle scroll events if needed
      // For example, infinite loading
    }, 100),
    []
  );

  if (!items.length) {
    return (
      <div 
        className={`flex items-center justify-center text-gray-500 ${className}`}
        style={{ height }}
      >
        No items to display
      </div>
    );
  }

  return (
    <div className={className} {...props}>
      <List
        height={height}
        itemCount={items.length}
        itemSize={itemHeight}
        itemData={itemData}
        overscanCount={overscanCount}
        width={width}
        onScroll={handleScroll}
      >
        {ListItem}
      </List>
    </div>
  );
}

// Variable size list for items with different heights
export function VariableSizeVirtualizedList({
  items = [],
  getItemHeight = () => 50,
  height = 400,
  width = '100%',
  renderItem,
  overscanCount = 5,
  className = '',
  ...props
}) {
  const listRef = useRef(null);
  
  // Memoize item data
  const itemData = useMemo(() => ({
    items,
    renderItem,
  }), [items, renderItem]);

  // Get item size callback
  const getItemSize = useCallback((index) => {
    return getItemHeight(items[index], index);
  }, [items, getItemHeight]);

  if (!items.length) {
    return (
      <div 
        className={`flex items-center justify-center text-gray-500 ${className}`}
        style={{ height }}
      >
        No items to display
      </div>
    );
  }

  return (
    <div className={className} {...props}>
      <VariableSizeList
        ref={listRef}
        height={height}
        itemCount={items.length}
        itemSize={getItemSize}
        itemData={itemData}
        overscanCount={overscanCount}
        width={width}
      >
        {ListItem}
      </VariableSizeList>
    </div>
  );
}

// Infinite scroll virtualized list
export function InfiniteVirtualizedList({
  items = [],
  itemHeight = 50,
  height = 400,
  width = '100%',
  renderItem,
  hasNextPage = false,
  isNextPageLoading = false,
  loadNextPage,
  threshold = 0.8,
  className = '',
  ...props
}) {
  const [isFetchingNextPage, setIsFetchingNextPage] = useState(false);
  const listRef = useRef(null);

  // Handle scroll for infinite loading
  const handleScroll = useCallback(({ scrollOffset, scrollDirection, scrollHeight }) => {
    if (
      hasNextPage &&
      !isNextPageLoading &&
      !isFetchingNextPage &&
      scrollOffset > scrollHeight * threshold
    ) {
      setIsFetchingNextPage(true);
      loadNextPage().finally(() => {
        setIsFetchingNextPage(false);
      });
    }
  }, [hasNextPage, isNextPageLoading, isFetchingNextPage, loadNextPage, threshold]);

  // Memoize item data
  const itemData = useMemo(() => ({
    items,
    renderItem,
  }), [items, renderItem]);

  // Loading indicator item
  const loadingItem = useMemo(() => ({
    isLoading: true,
  }), []);

  // Combined items with loading indicator
  const combinedItems = useMemo(() => {
    if (isNextPageLoading) {
      return [...items, loadingItem];
    }
    return items;
  }, [items, isNextPageLoading, loadingItem]);

  // Enhanced render item for infinite list
  const enhancedRenderItem = useCallback((item, index) => {
    if (item.isLoading) {
      return (
        <div className="flex items-center justify-center p-4">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">Loading more items...</span>
        </div>
      );
    }
    return renderItem(item, index);
  }, [renderItem]);

  // Update item data when render function changes
  const enhancedItemData = useMemo(() => ({
    items: combinedItems,
    renderItem: enhancedRenderItem,
  }), [combinedItems, enhancedRenderItem]);

  if (!items.length && !isNextPageLoading) {
    return (
      <div 
        className={`flex items-center justify-center text-gray-500 ${className}`}
        style={{ height }}
      >
        No items to display
      </div>
    );
  }

  return (
    <div className={className} {...props}>
      <List
        ref={listRef}
        height={height}
        itemCount={combinedItems.length}
        itemSize={itemHeight}
        itemData={enhancedItemData}
        overscanCount={overscanCount}
        width={width}
        onScroll={handleScroll}
      >
        {ListItem}
      </List>
    </div>
  );
}

// Masonry virtualized grid for variable height items
export function MasonryVirtualizedGrid({
  items = [],
  columnCount = 3,
  columnWidth = 300,
  gutter = 16,
  renderItem,
  height = 400,
  className = '',
  ...props
}) {
  const [columns, setColumns] = useState([]);
  const containerRef = useRef(null);

  // Organize items into columns
  useEffect(() => {
    const newColumns = Array.from({ length: columnCount }, () => []);
    const columnHeights = new Array(columnCount).fill(0);

    items.forEach((item, index) => {
      // Find shortest column
      const shortestColumnIndex = columnHeights.indexOf(Math.min(...columnHeights));
      newColumns[shortestColumnIndex].push(item);
      
      // Update column height (would need actual item height)
      // For now, estimate based on index
      columnHeights[shortestColumnIndex] += 100; // Estimated height
    });

    setColumns(newColumns);
  }, [items, columnCount]);

  if (!items.length) {
    return (
      <div 
        className={`flex items-center justify-center text-gray-500 ${className}`}
        style={{ height }}
      >
        No items to display
      </div>
    );
  }

  return (
    <div 
      ref={containerRef}
      className={`flex gap-${gutter/4} ${className}`}
      style={{ height }}
      {...props}
    >
      {columns.map((column, columnIndex) => (
        <div 
          key={columnIndex} 
          className="flex-1"
          style={{ width: columnWidth }}
        >
          {column.map((item, itemIndex) => (
            <div 
              key={item.id || itemIndex} 
              className="mb-4"
              style={{ marginBottom: gutter }}
            >
              {renderItem(item, columnIndex * columnCount + itemIndex)}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

// Utility function for throttling
function throttle(func, delay) {
  let timeoutId;
  let lastExecTime = 0;
  
  return function (...args) {
    const currentTime = Date.now();
    
    if (currentTime - lastExecTime > delay) {
      func.apply(this, args);
      lastExecTime = currentTime;
    } else {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        func.apply(this, args);
        lastExecTime = Date.now();
      }, delay - (currentTime - lastExecTime));
    }
  };
}

import { memo, useState } from 'react';
import { VariableSizeList } from 'react-window';
